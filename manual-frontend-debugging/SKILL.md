---
name: manual-frontend-debugging
description: Use when debugging a browser UI bug is faster through user repro plus temporary runtime probes than through full automation, and the agent should inspect event flow or state-sync logs instead of doing design, implementation, or routine browsing work.
homepage: https://github.com/GuoLuPM/skills
---

# Manual Frontend Debugging

## Overview

This is a frontend debugging skill only. The agent switches from repeated browser automation to user-driven reproduction, adds short-lived runtime probes, and diagnoses the bug from captured event flow.

## Use When

- The user can reproduce the bug reliably or semi-reliably.
- Timing, hover, focus, partial refresh, or state-sync behavior matters.
- Browser automation is unstable, slow to write, or slower than the user's manual repro.
- The main question is "which branch actually ran?" rather than "what does the UI look like?"

## Do Not Use

- A stable automated repro already exists.
- The issue is backend-only, terminal-only, or not a browser UI problem.
- The task is routine browsing, screenshots, or form filling.
- The task is UI design, visual review, page implementation, or styling work.

## Workflow

1. Pick 1 to 3 observation points before guessing the fix.
2. Add temporary runtime probes only. Do not commit permanent debug logging.
3. Limit logs to one click chain or one gesture chain.
4. Ask the user to reproduce once, then wait.
5. Read logs in order: entry -> branch -> state write -> refresh, close, or exit.

## Probe Rules

- Prefer runtime injection through DevTools, browser MCP, or script execution.
- Keep each log line single-line and low volume.
- For high-frequency hover or move events, log counters or first and last samples only.
- Probe only the few function boundaries that can explain the bug.

Recommended fields:

```text
seq, fn, branch, point, boxIndex, candidateCount, selectedBoxIndex, hoverBoxIndex
```

## User Prompts

Use direct prompts such as:

- "I've added short-lived probes. Reproduce once and tell me when you're done."
- "I'm only watching these 3 functions. Follow the same path 2 or 3 times, then send me the signal."
- "Logs are limited to one click chain. You can start now."

## Read Logs In This Order

1. Did the action enter the intended handler?
2. Were the key parameters correct?
3. Which guard, fallback, or branch diverted execution?
4. Which write produced the wrong state?
5. Which refresh, close, or exit followed?

## Guardrails

- Do not commit debug logs to the repo.
- Do not add broad, unrelated probes.
- Do not refactor before the user has reproduced the issue.
- This skill defines a collaboration pattern, not a guarantee that the agent can attach to the current browser session.
- Remove or disable temporary probes after diagnosis.
