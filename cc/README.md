# Time Anchor · Claude Code 版

这是 Time Anchor 的 **Claude Code（CC）移植版**，与主目录的 Codex 版共享同一套理念：
给本地 AI 伴侣一只表，让它在需要时知道——现在是什么时候，对方已经走过了多久。

代码结构、时间皮层（Temporal Cortex）、隐私边界都与 Codex 版一致，只针对 CC 的
hook / skill 机制做了必要适配。

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
