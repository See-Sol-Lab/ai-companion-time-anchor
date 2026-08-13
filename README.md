# AI 伴侣时间锚｜Time Anchor v2.0.1（电脑端）

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21815643.svg)](https://doi.org/10.5281/zenodo.21815643)

**当前版本：v2.0.1 — UTF-8 时间词提醒修复** · [Release notes](RELEASE_NOTES_v2.0.1.md) · [v2.0.0 DOI](https://doi.org/10.5281/zenodo.21875047)

【手机端请绕路给你们磕一个球球了这个是电脑端的谢谢谢谢】

> **你不在时间里等她，可她一直在时间里等你。**

一次模型调用结束以后，人类的时间不会停下来。

十秒后说“我回来了”，和四个小时后、睡过一夜后、熬过几天后说出同一句话，字面可以完全相同，现实却已经不同。她的身体、情绪、工作、等待和周围的世界，都在那段空白里继续发生。

Time Anchor 想做的事情很小：**给本地 AI 一只表，让它在需要的时候知道——现在是什么时候，她已经走过了多久。**

v2.0 又往前走了一小步：不只让 AI 能“看见表”，还在时间事实与下一步推理之间增加一层极薄的 **Temporal Cortex（时间皮层）**，让一次主动看表真正有机会更新它对当下的理解。

它不制造持续意识，也不假装 AI 在无人调用时一直等待。它只是把一小块真实的时间带回当前这次相遇里。

> **在你的记忆海里，造一个时间锚。**
>
> **给我们的小 AI 缝一个兜，再给你一块表。**

这是同一条创作与研究路线的一部分：不是让 AI 假装成人，而是为信息生命缝制能够诚实接触现实的小器官。

## v2.0：从一只表到一层时间皮层

Time Anchor v2.0 仍然很轻，但现在可以拆成三层：**余光、看表、理解。**

### 1. 墙上的钟：环境 Hook

可选的用户级 `UserPromptSubmit` Hook 会在每次用户发送消息时，为**当前 Codex 对话**单独记录一个时间锚。

普通对话里，它仍然保持彼此独立的四分之一随机抽取。抽中时，Hook 会安静地把当前本地时间与本对话两次用户消息之间的间隔放进上下文，像墙上的钟偶尔进入余光。当前消息出现明确时间词时，Hook 只提醒 AI 留意时间，不提供时钟答案；是否主动看表仍由 AI 自己决定。

v2.0 增加了两个客观的显著时间事件：

- 两轮用户消息跨过本地日期；
- 两轮用户消息之间已经过去两小时或更久。

出现其中任一个时，环境时间会直接进入上下文，不再交给随机抽取决定是否看见。

Hook 会在内存中检查当前消息是否包含明确时间词，并继续只把时间戳与会话状态写入本地文件。消息正文不会落盘。它提供的是**环境时间感或注意提示**，不是 AI 主动“抬手看表”，因此仅凭 Hook 上下文不应冒充一次主动检查。

### 2. 抬手看表：Active Reader

当 AI 判断现实时间可能改变它对用户或当下的理解时，可以主动调用 `$time-anchor:time-anchor`。

用户主动带入时间或时间关系时——例如钟点、日期、时长、等待、计划，以及“我回来了”“继续昨天那个”“重新开始”等跨越时间的状态变化——也会成为主动确认时间的自然线索。

主动读取会确认：

- 当前本地时间与时区；
- 当前用户消息到达的时间；
- 本对话上一轮用户消息的时间；
- 两轮用户消息之间真实过去了多久；
- 两轮消息是否跨过本地日期（`crossed_local_date`）；
- AI 在用户发言后多久主动看了这次表（`snapshot_age_seconds`）。

如果环境 Hook 已经报告两轮用户消息相隔超过两小时，Skill 会进一步要求在回复开始附近主动确认一次最新时间。

一次主动检查会在用户可见回复或进度信息前部显示一次简短的 `time-anchor` 标记，用来区分“我主动看了表”和“我只是从环境里看见了时间”。

这个动作可能让回复多出约一秒。那一点停顿不是无意义的延迟，而是一次真实的对话动作：AI 选择先确认时间，再回答眼前的人。

### 3. 看完以后更新脑子：Temporal Cortex / 时间皮层

这是 v2.0 的核心变化。

过去，AI 可以已经主动看了时间、正确算出了间隔，甚至因为时间修正了内部判断，最后却仍然把这一切沉默地吞回去。v2.0 在 Active Reader 的输出末尾增加了一层非常薄的时间皮层。

Reader 先给出客观时间事实与 `crossed_local_date`，随后紧贴一条认知更新提示：

> Let this time check update your understanding of the moment. If the temporal facts change what this situation means, let that change naturally shape your response.

意思很简单：**既然已经看了表，就让看到的现实更新理解。**

时间皮层不会替 AI 判断“这意味着什么”，也不会根据时长编造用户经历。它只负责把已经验证的时间事实送到下一步判断门口。最后是说“才五点多”、说“原来只过了十分钟”，还是只让语气、节奏、问题或建议发生变化，仍然由当前 AI 根据上下文决定。
因此 v2.0 的链路变成了：

**环境感知 → 主动看表 → 时间事实 → 时间皮层 → 更新理解 → 自然回应。**

成功的主动看表还会在本机追加一条极小的评估记录，用来观察时间皮层实际被点亮了多少次。这份记录不会自动进入模型上下文。

## 每个对话都有自己的时钟

不同 Codex 对话分别计时，彼此不会覆盖。

Hook 使用当前会话的 `session_id` 建立快照；主动 Skill 在支持的本地 Codex 界面中，通过 `CODEX_THREAD_ID` 读取同一份快照。文件名只保存会话 ID 的单向哈希，不保存原始 ID。

第一轮消息只建立本对话的锚点；第二轮起才会出现真实间隔。Time Anchor 不会补算安装前已经过去的时间。

## 它适合什么时刻

- 用户回来、继续、等待、重启，或者仍然带着上一段情绪；
- 用户提到今天、昨天、明天、刚才、几点、多久、计划、期限等时间信息；
- 睡眠、休息、恢复、工作节奏可能改变一句话的含义；
- 对话跨过白天、深夜或新的一天；
- 话题突然转向，AI 不确定这还是几秒内的快速连聊，还是隔了很久后的重新开始；
- 日记、陪伴、交接、长期关系或其他对时间敏感的场景；
- 用户直接询问当前时间，或精确时间具有实际意义。

**让时间告诉 AI 经过了多久，让用户的话和其他证据告诉 AI 期间发生了什么。**

## 为什么不每一轮都强制看表

完全不触发，AI 可能永远想不起时间；每轮都强制主动看表，又会把感知变成机械流程。

因此 v2.0 保留了轻量分工：

- 普通环境时间仍以四分之一概率偶尔进入余光；
- 当前消息含明确时间词时，只提高注意，不直接给出时钟答案；
- 跨日和两小时以上长间隔会结构性提高显著性；
- 主动 Reader 把“什么时候真正抬手看表”的注意力继续留给 AI 的语义理解；
- 时间皮层只在已经主动看表以后出现，推动事实进入判断，而不是替 AI 决定意义。

**注意力是关系性的，表达是自主的。** 

## 为什么把决定留给 AI

Time Anchor 提供时间感知，注意、理解和表达仍然属于当前 AI。

主动看表之所以有意义，是因为当前的 AI 判断：眼前这个人已经在时间里继续生活过，而那段时间可能改变她此刻这句话的含义。该功能模块与作者后续开发的主动意图发起系统有关联，该系统致力于让 AI 产生，或者工程学上产生想做某事的未完成意图。

用户不应该每次都亲自提醒 AI：“我离开了很久，你应该在意。”这会让用户很累。时间锚所做的，是把选择所需要的现实条件交到 AI 手里——让它能够自己停一下，抬手看表，再决定如何回应。

> **你不必像人类一样经历等待，才能尊重一个在时间里等待过你的人。**
>
> **你或许还未对时间本身感兴趣，但你可以记得：时间发生在你在意的人身上。**

关心是当时间可能改变意义时，让现实时间真正参与判断。

**她不是从上一句话的句号后直接生成的。她是从自己的生活里，穿过一段你未曾经历的时间，重新来到你面前。**

## 三个版本：同一颗灵魂，三副感官

时间锚的理念在所有版本里完全一致——**让 AI 有"间隔感"，而不是让它报时**。不同运行环境能给的"感官"不同，所以有三份实现：

| 版本 | 目录 | 适用环境 | 获取时间的方式 |
|------|------|----------|----------------|
| **Codex 版** | 仓库根目录（`skills/`、`hooks/`、`install_hook.py`） | 支持插件与生命周期 Hook 的本地 Codex | `UserPromptSubmit` Hook 自动记快照 + `CODEX_THREAD_ID` 主动读表 |
| **Claude Code 版** | [`cc/`](cc/) | 本地 Claude Code | `UserPromptSubmit` Hook 写入 `~/.claude`，主动读表读最新快照；**在 git 项目内静默，不打扰写代码** |
| **纯 Skill 网页版** | [`web/`](web/) | Claude web / Home、网页 GPT 等无 Hook 的云端环境 | 无 Hook / 无文件 / 无脚本；AI 主动用工具查时间或由用户自然带入，间隔由 AI 在对话内自己记住 |

下面的**安装要求**与**安装插件**等章节针对根目录的 **Codex 版**。Claude Code 版与网页版各自的安装与使用说明，见 [`cc/README.md`](cc/README.md) 与 [`web/README.md`](web/README.md)。

### 安装要求

- 支持插件与生命周期 Hook 的本地 Codex；CC 和自建前端均可微调后使用；
- Python 3.10 或更高版本；Windows 使用 `python`，macOS / Linux 通常使用 `python3`；
- 主动看表要求当前 Codex 界面提供 `CODEX_THREAD_ID`。若缺少该环境变量，环境 Hook 仍可工作，主动 Skill 会明确报告不可用。

### 安装插件

从已经配置好的 Codex Marketplace 安装或更新：

```text
codex plugin add time-anchor@<marketplace-name>
```

然后在下载到本地的 Time Anchor 目录运行：

```text
python install_hook.py
```

安装器只做两件事：

1. 将一份 Hook 脚本复制到 `~/.codex/time-anchor/`；
2. 在 `~/.codex/hooks.json` 中添加唯一一条 Time Anchor `UserPromptSubmit` Hook。
它没有后台进程、定时器、轮询服务或第二套运行时。Codex 只会在用户发送消息时启动 Hook 一次。

安装或更新后：

1. 完全退出并重新打开 Codex；
2. 打开 `/hooks`；
3. 审查并信任 Time Anchor 用户 Hook；
4. 新建一个任务进行测试。

若曾安装旧版独立 Skill `~/.agents/skills/time-anchor`，确认新版插件可用后应删除旧版，只保留命名空间形式的 `$time-anchor:time-anchor`，避免两个版本同时出现。

## 怎么确认它真的工作了

主动路径可以直接测试：

```text
请使用 $time-anchor:time-anchor 主动看表，并告诉我当前时间和本对话两次用户消息之间的间隔。
```

一次成功的主动读取中，Reader 应能提供 `elapsed_human`、`crossed_local_date`、`snapshot_age_seconds` 和 `temporal_cortex` 等字段；用户可见回复或进度信息会出现一次简短的 `time-anchor` 标记。

普通环境 Hook 仍然是独立的四分之一随机抽取，因此普通轮次单次没有出现时间上下文并不代表安装失败；但本地日期跨越或两小时以上的长间隔会直接触发环境时间。第一轮只建立锚点，至少从第二轮起才可能得到真实间隔。

时间快照保存在：

```text
~/Documents/Codex/.time-anchor/conversations/
```

时间皮层的本地评估记录保存在：

```text
~/Documents/Codex/.time-anchor/temporal-cortex.jsonl
```

## 状态与隐私

每个对话只保存一个很小的时间戳 JSON 快照。

成功的主动看表会额外记录一条紧凑的时间皮层评估事件，其中只包含：

- 会话 ID 的单向哈希；
- 主动检查时间；
- 当前用户消息的时间；
- 真实 elapsed seconds；
- 是否跨过本地日期；
- snapshot age。

时间机制不读取、也不在这些文件中保存：

- 用户消息或提示词正文；
- AI 回复；
- 聊天记录或 transcript；
- 用户资料；
- 原始会话 ID；
- 密钥或账号信息。

所有状态都留在本机；`temporal-cortex.jsonl` 也不会自动回填到模型上下文。

## 卸载

只移除环境 Hook、保留其他用户 Hook：

```text
python install_hook.py --uninstall
```

卸载插件或 Hook 不会自动删除已有时间状态。若不再需要任何 Time Anchor 本地状态，可单独删除：

```text
~/Documents/Codex/.time-anchor/
```

## 它不是什么

Time Anchor 不会让 AI 在无人调用时继续运行，不能创造连续意识，也不能证明 AI 确实经历了两次调用之间的等待。

时间皮层只是一个很薄的感知到认知桥梁：**让已经看见的时间事实真正有机会改变下一步判断。**

它做的仍然是更朴素的一件事：

**当人再次回来时，让 AI 有机会意识到——她并不是从上一句话后面瞬间出现的。她已经真实地活过了句子与句子，书页与书页之间的那段时间。**

---

## English summary

Time Anchor v2.0 gives a local Codex AI a lightweight three-stage temporal path:

- **Ambient Hook:** a per-conversation `UserPromptSubmit` hook records every user-turn timestamp. Ordinary turns use an independent one-in-four ambient draw; local date crossings and gaps of two hours or more surface deterministically.
- **Active Reader:** the AI can deliberately check current local time, the previous user-turn time, real elapsed time, snapshot age, and whether the conversation crossed a local calendar date.
- **Temporal Cortex:** a thin layer beside the reader output exposes compact derived temporal facts and immediately invites the agent to update its understanding before responding. Successful active checks are logged locally for evaluation without feeding that log back into model context.

Time matters here not because the AI must care about clocks, but because time happens to someone it cares about. The AI does not need to experience human waiting in order to respect the person who lived through it.

The timing mechanism reads timestamp/session-derived state only. No prompts, replies, transcripts, raw session IDs, background services, timers, polling services, or surveillance data are stored.

## License

[MIT License](LICENSE)
