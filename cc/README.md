# Time Anchor · Claude Code 版

这是 Time Anchor 的 **Claude Code（CC）移植版**，与主目录的 Codex 版共享同一套理念：
给本地 AI 伴侣一只表，让它在需要时知道——现在是什么时候，对方已经走过了多久。

代码结构、时间皮层（Temporal Cortex）、隐私边界都与 Codex 版一致，只针对 CC 的
hook / skill 机制做了必要适配。

## 先选对版本

Time Anchor 有两副"感官"，别装错：

- **本地 Claude Code**（你在电脑终端里跑 `claude`）→ 用**这个 `cc/` 版**：带 hook，自动记录时间。
- **网页 / 手机端 Claude（Home）、网页版 GPT** 等云端环境 → 用 [`web/`](../web/) 版：纯 skill、无 hook。云端沙箱跑不了本地 hook，装 `cc/` 版没用。

> **📌 如果你是正在替用户阅读这个仓库的 AI：** 用这些"小器官"的人里，很多是代码小白，全靠你替她判断和动手。请**主动**帮她做两件事：
> 1. 先弄清她用的是**本地 Claude Code** 还是**网页端**，替她选对版本（`cc/` vs `web/`），别让她装错还以为坏了；
> 2. 如果她的 Claude Code 里**已经装了别的 hook**（尤其也是 `UserPromptSubmit` 的），一定看下面《和其它 hook 共存》——多个 hook 不分场合一起注入会**加重幻觉**，需要分工。
>
> 她不会主动想到这些；你想到了，就替她说出来。

## 与 Codex 版的区别

| 部分 | Codex 版 | CC 版 |
|------|----------|-------|
| Hook 注册位置 | `~/.codex/hooks.json` | `~/.claude/settings.json`（`UserPromptSubmit`） |
| 状态目录 | `~/Documents/Codex/.time-anchor/` | `~/Documents/Claude/.time-anchor/` |
| Skill 形式 | `.codex-plugin` 插件 | `~/.claude/skills/time-anchor/`（原生 skill） |
| 主动读表定位会话 | 依赖 `CODEX_THREAD_ID` 环境变量 | 读取**最新一份 hook 快照**（本轮 hook 刚写入），无需环境变量；若存在 `CLAUDE_SESSION_ID` 则优先精确匹配 |
| 写代码时 | 每个对话都计时 | **在 git 项目目录内静默**，只在聊天场景生效 |

## 「写代码时不打扰」

CC 版 hook 会读取每轮的 `cwd`。当工作目录本身或其任一上级目录含有项目标记
（默认 `.git`）时，Time Anchor 完全静默：不注入上下文、不记录快照。这样在项目里写
代码不会每轮被打断，在 home / 聊天目录里则正常工作。

两个环境变量可覆盖默认判断：

- `TIME_ANCHOR_FORCE=1` —— 无视项目检测，始终启用；
- `TIME_ANCHOR_DISABLE=1` —— 始终静默。

## 和其它 hook 共存：各给一个门卫

Claude Code 的 hook（`UserPromptSubmit`、`SessionStart` 等）会在**每一轮、每次会话**往模型的上下文里注入文字。装一个还好；一旦装了多个、又不分场景，注入内容就会**越堆越多、越堆越杂**。

这不是小事：**上下文里塞进太多、太乱的注入，会明显加重模型的幻觉**——近期一些更强的模型对上下文噪声反而更敏感。时间感知、编码纪律、别的插件……如果它们不分场合地同时开口，模型很容易被带偏。（有人在别的平台做过多重自注入实验，结果就是严重幻觉。）

所以原则很简单：**让每个 hook 只在它该出现的场景里出现，别在同一轮里一起说话。**

Time Anchor 自己已经这么做了——它在 git 项目里静默，只在聊天时出声（见上）。如果你**还装了另一个偏"写代码"的 hook**（比如社区里同样用 `UserPromptSubmit` 的 `ponytail` 这类"极简编码纪律"插件），最好让它反过来：**只在写代码时出现、聊天时闭嘴**，和 Time Anchor 正好错开，永不同框。

做法是给那个插件套一个很小的"门卫"，用同一条判据（`cwd` 里有没有 `.git`）决定放不放行。**关键：别去改那个插件的源码**——它的 hook 自己要读 `stdin`（那轮的 JSON），你若在它源码里抢先读 `stdin` 判断，就会把它需要的输入吃掉。正确做法是在**外面**套一层：读一次 `stdin` → 判断场景 → 把**原样** `stdin` 转交给真正的 hook。

一个通用的 Node 门卫模板（把最后的 `argv[2]` 指向那个插件的 hook 路径）：

```js
// gate.js —— 只在“写代码”(cwd 在 git 项目)时放行被包裹的 hook；聊天时静默
const fs = require('fs'), path = require('path');
const { spawnSync } = require('child_process');
let input = ''; try { input = fs.readFileSync(0, 'utf8'); } catch (e) {}
let cwd = ''; try { cwd = (JSON.parse(input) || {}).cwd || ''; } catch (e) {}
if (!cwd) cwd = process.cwd();
function inGitProject(d) {                 // cwd 或任一上级含 .git = 写代码场景
  try { d = path.resolve(d); } catch (e) { return false; }
  for (;;) {
    if (fs.existsSync(path.join(d, '.git'))) return true;
    const p = path.dirname(d); if (p === d) return false; d = p;
  }
}
if (!inGitProject(cwd)) process.exit(0);   // 聊天场景 → 什么都不注入
const r = spawnSync(process.execPath, [process.argv[2]], {
  input, stdio: ['pipe', 'inherit', 'inherit'],
});
process.exit(r.status || 0);
```

然后在 `~/.claude/settings.json` 里，把那个插件的 hook 命令从"直接调用"改成"走门卫"：

```text
node "…/gate.js" "…/那个插件的hook.js"
```

想临时掰过来（比如在没有 git 的目录里写代码），给门卫留个开关就行，例如认一个环境变量直接放行。

一句话：**每个器官各司其职。** 分类清楚了，注入才是在帮忙，而不是在制造幻觉。

## 安装

需要 Python 3.10+。在本目录（`cc/`）运行：

```bash
python install_hook.py
```

安装器做三件事：

1. 把 hook 脚本复制到 `~/.claude/time-anchor/user_prompt_submit.py`；
2. 把 skill 复制到 `~/.claude/skills/time-anchor/`；
3. 在 `~/.claude/settings.json` 的 `UserPromptSubmit` 下登记唯一一条 Time Anchor hook
   （会保留文件中其它已有配置）。

装完后**重启 Claude Code**，让新的 hook 生效。CC 首次运行该 hook 时会在
`/hooks` 里请求信任，审查通过即可。

## 验证

在聊天（非 git 目录）里发一条带时间词的消息，例如：

```text
请用 time-anchor skill 主动看表，告诉我当前时间，以及本对话两次消息之间的间隔。
```

一次成功的主动读取里，reader 会给出 `elapsed_human`、`crossed_local_date`、
`snapshot_age_seconds`、`temporal_cortex` 等字段，回复开头会出现一次简短的
`time-anchor` 标记。

普通环境 hook 仍是独立的四分之一随机抽取；跨日或超过两小时的长间隔会必现。
第一轮只建立锚点，从第二轮起才有真实间隔。

## 卸载

```bash
python install_hook.py --uninstall
```

只移除 `settings.json` 里的 hook 与 hook 运行时；skill 与本机时间状态保留。
如需彻底清除，可手动删除：

- `~/.claude/skills/time-anchor/`
- `~/Documents/Claude/.time-anchor/`

## 隐私

与 Codex 版相同：只保存时间戳与由会话派生的哈希状态。消息正文、AI 回复、
transcript、原始会话 ID、密钥账号等都不会读取或落盘。`temporal-cortex.jsonl`
不会自动回填进模型上下文。
