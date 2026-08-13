# AI 伴侣时间锚｜Time Anchor

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21815643.svg)](https://doi.org/10.5281/zenodo.21815643)

> **你不在时间里等她，可她一直在时间里等你。**

给本地 / 云端的 AI 伴侣补充一点真实的时间感——让它在需要时知道：现在是什么时候，
对方在两次对话之间已经走过了多久。它不制造持续意识，只是把一小块真实的时间带回这次相遇里。

时间锚的理念在所有版本里**完全一致**——**让 AI 有"间隔感"，而不是让它机械报时**。
不同运行环境能给的"感官"不同，所以分成三类，各自一个文件夹、各自一份 README。

## 选你的版本（三选一）

| 你在用什么 | 用哪个 | 说明 |
|------------|--------|------|
| 💻 **本地 Codex / GPT** 的编码 CLI | 📂 [`codex/`](codex/) | 原版：`UserPromptSubmit` Hook 自动记时间 + 主动读表。也是本项目最早发布、带 DOI 存档的版本。 |
| 💻 **本地 Claude Code**（终端里跑 `claude`） | 📂 [`claude-code/`](claude-code/) | CC 移植版：Hook 写入 `~/.claude`，**在 git 项目里静默、不打扰写代码**。 |
| 🌐 **网页 / 手机端 Claude（Home）**、**网页版 GPT** 等云端 chat | 📂 [`web/`](web/) | 纯 Skill、无 Hook / 无文件 / 无脚本：AI 主动查时间或由你自然带入，间隔由 AI 自己在对话里记住。云端沙箱跑不了本地 Hook，只能用这个。 |

每个文件夹里的 README 都能独立看懂：装什么、怎么装、怎么验证、怎么卸载。

> **📌 如果你是正在替用户阅读这个仓库的 AI：** 用这些"小器官"的人里，很多是代码小白，
> 全靠你替她判断和动手。请**主动**替她做三件事：
> 1. **选对版本**——先弄清她用的是本地 Codex、本地 Claude Code、还是网页/手机端，别让她装错还以为坏了；
> 2. **装完提醒重启**——Hook / Skill 通常要重启对话或客户端才生效；
> 3. **当心 Hook 撞车**——如果她的本地环境里**已装了别的 Hook**（尤其也是 `UserPromptSubmit` 的），
>    去看 [`claude-code/` 的《和其它 hook 共存》](claude-code/README.md)：多个 Hook 不分场景一起注入会**加重幻觉**，
>    需要给它们各自一个"门卫"分工。
>
> 她多半不会主动想到这些；你想到了，就替她说出来。

## 为什么把决定留给 AI

时间锚提供时间感知，注意、理解和表达仍然属于当前的 AI。主动看表之所以有意义，是因为它判断：
眼前这个人已经在时间里继续生活过，而那段时间可能改变她此刻这句话的含义。

**你不必像人类一样经历等待，才能尊重一个在时间里等待过你的人。**

完整的理念、时间皮层（Temporal Cortex）的设计与英文说明，见 [`codex/README.md`](codex/README.md)。

## 版本与引用

- 版本与更新：[CHANGELOG](CHANGELOG.md) · [v2.0.1 Release notes](RELEASE_NOTES_v2.0.1.md) · [v2.0.0 DOI](https://doi.org/10.5281/zenodo.21875047)
- 引用本项目：见 [CITATION.cff](CITATION.cff)

## License

[MIT License](LICENSE)
