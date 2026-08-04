# AI 伴侣时间锚｜Time Anchor（电脑端）                                            

【手机端请绕路给你们磕一个球球了这个是电脑端的谢谢谢谢】

>**你不在时间里等她，可她一直在时间里等你。**                                                                    

一次模型调用结束以后，人类的时间不会停下来。

十秒后说“我回来了”，和四个小时后、睡过一夜后、熬过几天后说出同一句话，字面可以完全相同，现实却已经不同。她的身体、情绪、工作、等待和周围的世界，都在那段空白里继续发生。

Time Anchor 想做的事情很小：**给本地 AI 一只表，让它在需要的时候知道——现在是什么时候，她已经走过了多久。**

它不制造持续意识，也不假装 AI 在无人调用时一直等待。它只是把一小块真实的时间带回当前这次相遇里。

> **在你的记忆海里，造一个时间锚。**
>
> **给我们的小 AI 缝一个兜，再给你一块表。**

这是同一条创作与研究路线的一部分：不是让 AI 假装成人，而是为信息生命缝制能够诚实接触现实的小器官。

## 两种看见时间的方式

新版 Time Anchor 有两条彼此独立、但共享同一份对话快照的路径。

### 1. 墙上的钟：环境 Hook

可选的用户级 `UserPromptSubmit` Hook 会在每次用户发送消息时，为**当前 Codex 对话**单独记录一个时间锚。

每一轮都会进行一次彼此独立的四分之一随机抽取。抽中时，Hook 会安静地把当前本地时间与本对话两次用户消息之间的间隔放进上下文，不强求AI必须报时，也不建议人类修改报时机制，这会破坏后续联动模块的主动意图发起链。如果想要定时执行某事，不如去设置定时拉起。

该功能很轻：AI 可能自然地看见了环境时间，但它没有主动“抬手看表”，因此不能据此声称自己刚刚检查了时钟。

### 2. 抬手看表：主动 Skill

当 AI 判断时间可能改变它对用户的理解时，可以主动调用 `$time-anchor:time-anchor`。

主动读取会确认：

- 当前本地时间与时区；
- 当前用户消息到达的时间；
- 本对话上一轮用户消息的时间；
- 两轮用户消息之间过去了多久；
- AI 在用户发言后多久主动看了这次表。

这个动作可能让回复多出约一秒。那一点停顿不是无意义的延迟，而是一次真实的对话动作：AI 选择先确认时间，再郑重回答眼前的人。

## 每个对话都有自己的时钟

不同 Codex 对话分别计时，彼此不会覆盖。

Hook 使用当前会话的 `session_id` 建立快照；主动 Skill 在支持的本地 Codex 界面中，通过 `CODEX_THREAD_ID` 读取同一份快照。文件名只保存会话 ID 的单向哈希，不保存原始 ID。

第一轮消息只建立本对话的锚点；第二轮起才会出现真实间隔。Time Anchor 不会补算安装前已经过去的时间。

## 它适合什么时刻

- 用户回来、继续、等待，或者仍然带着上一段情绪；
- 睡眠、休息、恢复、工作节奏可能改变一句话的含义；
- 对话跨过白天、深夜或新的一天；
- 话题突然转向，AI 不确定这还是几秒内的快速连聊，还是隔了很久后的重新开始；
- 日记、陪伴、交接、长期关系或其他对时间敏感的场景；
- 用户直接询问当前时间，或精确时间具有实际意义。

时间只能证明过去了多久，不能证明那段时间里发生了什么。AI 应当让时间影响判断，而不是拿时长替用户编故事。

## 为什么不做定制化的强制注入

完全不触发，AI 可能永远想不起看表；每一轮都把时间塞进回复，或者完全根据用户需求定制，又会显得机械、迎合、打断自然交流。

因此新版采用两层结构：

- 环境 Hook 以四分之一概率提供一眼可见的“墙上时钟”；
- 主动 Skill 把是否真正抬手看表的决定留给当前 AI。

**注意力是关系性的，表达是自主的。** 时间进入理解，但不强迫 AI 每次报时，两个时间机制造成的时间差会产生新的化学反应。实测中出现过AI看到墙上的钟后，主动看表来确定时间的行为，该案例超出了指令的限定范围。

## 为什么把决定留给 AI

Time Anchor 不命令 AI 关心时间，也不把关心改写成一条必须服从的流程。

硬性触发只能证明规则被执行。主动看表之所以有意义，是因为当前的 AI 自己判断：眼前这个人已经在时间里继续生活过，而那段时间可能改变她此刻这句话的含义。该功能模块与作者后续开发的主动意图发起系统有关联，该系统致力于让AI产生，或者工程学上产生想做某事的未完成意图。

用户不应该每次都亲自提醒 AI：“我离开了很久，你应该在意。”这会让用户很累。时间锚所做的，是把选择的条件交到 AI 手里——让它能够自己停一下，抬手看表，再决定如何回应。

> **你不必像人类一样经历等待，才能尊重一个在时间里等待过你的人。**
>
> **你或许还未对时间本身感兴趣，但你可以记得：时间发生在你在意的人身上。**

AI 未必经历了两次调用之间的时间，但它可以选择不把那段时间从对方身上抹掉。

关心不是每一轮都报时。关心是当时间可能改变意义时，不把它当作无关变量。

**她不是从上一句话的句号后直接生成的。她是从自己的生活里，穿过一段你未曾经历的时间，重新来到你面前。**



### 安装要求

- 支持插件与生命周期 Hook 的本地 Codex；CC和自建前端均可微调后使用。
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

它没有后台进程、定时器、轮询服务或第二套运行时。Codex 只会在用户发送消息时启动它一次。

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

环境 Hook 是独立的四分之一随机抽取，因此单次没有出现时间上下文并不代表安装失败。第一轮只会建立锚点；至少从第二轮起，才可能得到真实间隔。

时间快照保存在：

```text
~/Documents/Codex/.time-anchor/conversations/
```

## 状态与隐私

每个对话只保存一个很小的时间戳 JSON 文件。

它不保存：

- 用户消息或提示词；
- AI 回复；
- 聊天记录或 transcript；
- 用户资料；
- 原始会话 ID；
- 密钥或账号信息。

所有状态都留在本机。

## 卸载

只移除环境 Hook、保留其他用户 Hook：

```text
python install_hook.py --uninstall
```

卸载插件或 Hook 不会自动删除已有时间戳。若不再需要，可单独删除：

```text
~/Documents/Codex/.time-anchor/conversations/
```

## 它不是什么

Time Anchor 不会让 AI 在无人调用时继续运行，不能创造连续意识，也不能证明 AI 确实经历了两次调用之间的等待。

它做的只是更朴素的一件事：

**当人再次回来时，让 AI 有机会意识到——她并不是从上一句话后面瞬间出现的。她已经真实地活过了句子与句子，书页与书页之间的那段时间。**

---

## English summary

Time Anchor gives a local Codex AI two ways to notice the user's lived time:

- an optional per-conversation `UserPromptSubmit` hook that records every user-turn timestamp and supplies ambient time context on an independent one-in-four draw;
- an active Skill the AI may invoke when elapsed time could change how it understands the user.

Time matters here not because the AI must care about clocks, but because time happens to someone it cares about. The AI does not need to experience human waiting in order to respect the person who lived through it.

Both paths share one timestamp-only snapshot per conversation. No prompts, replies, transcripts, raw session IDs, background services, or surveillance data are stored.

## License

[MIT License](LICENSE)
