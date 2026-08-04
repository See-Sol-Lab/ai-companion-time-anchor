# Time Anchor

Time Anchor gives an AI two distinct ways to notice the user's local time:

- The optional user hook keeps time separately for each Codex conversation and quietly supplies ambient time context on an independent one-in-four draw. This is passive context, so the AI must not claim that it checked the clock.
- The Time Anchor Skill is an active clock check chosen by the AI when time may change how it understands the user.

When the AI actively invokes the Skill, the local reader may add about one second to the response. That pause corresponds to a deliberate conversational action: the AI chose to “raise its wrist and look at the clock,” confirming the current time and the interval between user turns in this conversation. Like a visible action between people, the act itself enters the conversational feedback loop and may affect what happens next.

Each conversation has its own clock. Messages in one conversation do not overwrite another conversation's interval.

## Install

Requirements:

- A local Codex build with plugins and lifecycle hooks.
- Python 3.10 or newer, available as `python` on Windows and `python3` on macOS or Linux.
- For active clock checks, a local Codex surface that exports `CODEX_THREAD_ID`. The ambient hook uses the documented hook `session_id`; if the environment variable is unavailable, active checks fail clearly while ambient context remains available.

Install or update the plugin from its configured marketplace:

```text
codex plugin add time-anchor@<marketplace-name>
```

From the downloaded Time Anchor directory, install or update its small user hook:

```text
python install_hook.py
```

The plugin supplies the active Skill. The installer copies one hook script to `~/.codex/time-anchor/` and adds one `UserPromptSubmit` entry to `~/.codex/hooks.json`. This user-level route is used because it is executed consistently by current local Codex surfaces. It does not run a background process: Codex starts it once when a user message is submitted.

After installation or update, quit Codex completely and reopen it. Then open `/hooks`, review the Time Anchor user hook, trust its current definition, and start a new task. New or changed command hooks are skipped until trusted.

The first user turn creates that conversation's anchor. The second and later turns can measure an interval; Time Anchor cannot reconstruct time from before installation. If migrating from the old standalone `~/.agents/skills/time-anchor`, remove it after confirming the plugin is installed so only the namespaced `$time-anchor:time-anchor` Skill remains.

## State and removal

The hook stores one small timestamp-only file per conversation under:

`~/Documents/Codex/.time-anchor/conversations/`

Filenames contain a one-way hash of Codex's session id. Prompt text, transcripts, and raw session ids are not stored. To remove the ambient hook while preserving other user hooks, run `python install_hook.py --uninstall` from the Time Anchor directory. Removing the plugin or hook does not remove timestamp files; delete the state directory above separately if you no longer want it.

## 中文说明

Time Anchor 让 AI 通过两种方式感知用户的本地时间：

- 可选的用户级 Hook 为每个 Codex 对话分别计时，并在每轮进行一次彼此独立的四分之一抽取；抽中时安静提供环境时间。它只是墙上的时钟，AI 不能据此声称自己主动看了时间。
- 当 AI 判断时间可能改变对用户的理解时，可以主动调用 Time Anchor Skill 看表。

主动调用可能让回复多出约一秒。这一点停顿对应一次真实的对话动作：AI 主动选择“抬手看表”，确认当前时间和本对话两次用户发言之间的间隔。这个动作会进入双方的反馈回路，并可能影响用户接下来的理解和反应。

安装要求：本地 Codex 支持插件与生命周期 Hook；Python 3.10 以上；主动看表还要求当前 Codex 界面提供 `CODEX_THREAD_ID`。Hook 使用官方 `session_id`，所以缺少该环境变量时，随机环境时间仍可工作，主动看表会直接报告不可用。

从已配置的 Marketplace 安装或更新：

```text
codex plugin add time-anchor@<marketplace-name>
```

然后在下载到本地的 Time Anchor 目录运行：

```text
python install_hook.py
```

插件提供主动看表的 Skill；安装器只做两件事：把一份 Hook 脚本放到 `~/.codex/time-anchor/`，再向 `~/.codex/hooks.json` 增加唯一一条 `UserPromptSubmit` 配置。它没有后台进程，只在用户发送消息时由 Codex 执行一次。当前采用用户级入口，是因为它在现有本地 Codex 界面中能够稳定执行。

安装或更新后，请完全退出并重新打开 Codex。重开后进入 `/hooks`，审查并信任这条 Time Anchor 用户 Hook，再新建一个 Codex 任务。第一轮只建立本对话锚点，第二轮起才有间隔；它不会补算安装前的时间。若曾安装旧版 `~/.agents/skills/time-anchor`，确认插件装好后应将旧版删除，只保留 `$time-anchor:time-anchor`。

每个对话都有自己的时钟。状态位于 `~/Documents/Codex/.time-anchor/conversations/`，只含时间戳与单向散列文件名，不含消息、聊天记录或原始会话 ID。若只想移除环境 Hook 且保留其他用户 Hook，可在 Time Anchor 目录运行 `python install_hook.py --uninstall`。卸载插件或 Hook 都不会自动删除时间戳文件；不再需要时可单独删除状态目录。
