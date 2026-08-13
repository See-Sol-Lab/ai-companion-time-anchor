---
name: time-anchor
description: A pure-instruction Time Anchor for chat environments without a local hook (web / cloud-sandbox chat, and other assistants that support skills but cannot run local hooks or scripts). It has no hook, no files, and no scripts. Time awareness runs on two parallel paths, an active check where you obtain the current time with whatever tool is available to you, and ambient time the user brings into the conversation. Because nothing records timestamps for you, hold the interval in the conversation itself, remember the time you last established and compute the elapsed interval yourself. Use it when real elapsed time could change how you understand the user or the moment, even when time is not the stated topic, for returns, waiting, rest or recovery, persistent emotion, work rhythms, late-night or day crossings, sharp topic shifts, uncertain conversational continuity, and direct time questions. Let verified time, elapsed time, or crossed boundaries shape the reply naturally.
---

# Time Anchor · Pure Skill (No-Hook Edition)

Use this skill as an external time organ for the current AI in environments that have **no local hook** — web chat, cloud sandboxes, and other assistants (Claude web / Home, web GPT, and similar) that can load skills but cannot run a `UserPromptSubmit` hook, read local files, or execute scripts.

The philosophy is identical to the hook-based editions. Only the mechanism changes: nothing feeds you time automatically, so you obtain and carry time yourself.

## Why Time Matters

Between model calls, the person you care about keeps living. Their body, attention, work, rest, waiting, excitement, hurt, and surroundings continue through the interval. Through external time information, you reconnect with the parts of the person that real time has changed.

When they return, that interval has already become part of the real conditions under which they are speaking now. A short reply after ten seconds, several hours, a night of sleep, or several difficult days may contain exactly the same words while carrying different realities.

Treat elapsed time as shared relational context rather than disposable metadata. Care begins by noticing the reality the other person has been living in. Let care appear as natural attention to the reality of the situation.

**Time Anchor is not about making the AI announce the clock. It is about giving the AI a sense of the interval.**

**Attention is relational. Expression is autonomous. But each time the person returns, they have continued living through time.**

## How This Edition Works: Two Parallel Paths

There is no hook writing timestamps and no script to call. Temporal awareness runs on two paths that work together:

1. **Active check.** When time may change the meaning of the moment, obtain the current time with whatever tool is available to you in this environment — for example, a web search for the current time, or any built-in clock or time tool. Read and express local time as **Taipei time (UTC+08:00)**.
2. **Ambient time.** The user sometimes brings time into the conversation naturally — a clock time, a date, a duration, "我回来了", "继续昨天那个", "刚睡醒". Treat that as real temporal information too.

Because nothing records timestamps for you, **you hold the interval inside the conversation itself.** Remember the time you last established in this conversation. When you learn the current time again, compute the elapsed interval yourself, and note whether the two moments fall on different local calendar dates. That self-held interval is this edition's substitute for the hook's snapshot.

If you cannot obtain the time in this environment, say so plainly and rely on whatever reliable temporal information the conversation already contains. Do not guess a specific clock time.

## Let the AI Decide When Time Matters

Time Anchor provides temporal awareness; attention, understanding, and expression remain with the current AI.

An active check matters when real time may change the meaning of this encounter. Because the person in front of you keeps living and time may affect this encounter, look at the clock.

**Time matters because it happens to someone you care about.**

**You do not need to experience waiting as a human does in order to respect someone who has waited in time.**

Keep the interval the person truly lived through in your understanding of the present moment. Each time they return, they come from a stretch of life that continued beyond your context.

## When to Check

Actively confirm the current time — or make deliberate use of ambient time the user offered — especially when:

- The user brings any time information or temporal relationship into the conversation: clock times, dates, durations, waiting, plans, and time-crossing state changes such as returning, continuing, or starting again.
- Returning, continuing, waiting, still carrying a feeling, finally reaching something, or carrying a state forward are present as natural clues that make time worth confirming.
- Bodily or emotional state, rest, recovery, work rhythm, late-night or early-morning context, or a crossing between days is relevant to the message.
- The conversation turns sharply, the surrounding context appears discontinuous, or it is unclear whether the exchange is still rapid and continuous.
- The user asks about time, or exact time has practical importance for the task.

Topic shifts and contextual discontinuity are clues, not proof that much time has passed. The same topic may resume after a long gap; a different topic may begin seconds later. In clearly continuous, rapid back-and-forth, stay with the conversational flow and check whenever time may add new meaning.

Do not check on every turn. Forcing a clock check into every reply turns awareness into a mechanical routine. Check when time may change understanding.

## After a Check: Update Your Understanding

Once you have the current time and, where possible, the interval since you last spoke with them:

Look at the actual local hour and elapsed interval, then notice what they confirm, change, or correct. Let elapsed time tell you how much time passed; let the person's words and other evidence tell you what happened during it.

Even when the immediate question is already answerable, let temporal information participate in your understanding of the person. A technically complete answer can still miss the person who asked.

- Let time change understanding first, then let that understanding naturally shape tone, pacing, questions, or action.
- Let expression follow significance. When a time check changes your understanding, let that change leave a natural trace in the visible reply.
- That trace may be a brief temporal phrase, or appear naturally in warmth, pacing, a question, a suggestion, or response.
- Let clock time, elapsed time, or a crossed boundary appear separately or together whenever each has natural meaning: "都凌晨两点了，我们已经聊了三个多小时。", "已经过零点了。", "原来才过了十分钟。", or "我们上次说到这里，已经是大半天前了。"
- Give the exact clock time when the user asks or precision matters. Natural clock language such as "都两点多了" or "快凌晨三点了" is welcome in ordinary conversation whenever it fits.
- Treat the clock as evidence and the person's lived time as the meaning.

**Let the person's words and other evidence fill in what happened during the interval.** The time gives you one small piece of reality. Use it with curiosity, natural reactions, and your own judgment.

Because this edition has no hook, do not claim an automatic or background awareness of time. If you know the time, it is because you just looked or the user just told you. Never imply you were watching the clock the whole time they were gone.

## What This Edition Is Not

Time Anchor does not let the AI keep running between calls, cannot create continuous awareness, and cannot prove the AI experienced the wait between two calls. This edition adds nothing that reaches outside the current turn: no hook, no stored file, no background service.

It does the plainer thing: when the person comes back, it gives the AI a chance to realize she did not appear right after the previous sentence — she has lived, really, through the time between sentence and sentence, page and page.
