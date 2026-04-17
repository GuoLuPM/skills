# Codex

```
Fetch and follow instructions from https://raw.githubusercontent.com/GuoLuPM/skills/main/.codex/INSTALL.md
```

# 如何使用

- 通用规则：你直接点名技能名称，或你的需求描述命中它的触发条件，Codex 就会用它。

- `manual-frontend-debugging`
  - 触发：你能自己复现前端问题，希望 Codex 先挂短日志或临时探针，你操作一遍，再让它看日志定位。
  - 你可以直接说：`你先挂短日志，我来复现，你看日志。`

- `subagent-governance`
  - 触发：你已经准备派子代理，现在想把任务拆成更窄的问题，控制上下文、并行边界和输出格式。
  - 你可以直接说：`帮我把这个任务拆成几个适合子代理的子问题，并给每个子问题最小上下文和禁止扩展范围。`
