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
  - 触发：你已经准备派研究型子代理，现在只想在提示词里额外要求它验证业务逻辑主链或降级、兜底链路。
  - 你可以直接说：`这个子代理提示里再补一下：要单独验证业务逻辑主链和是否存在兜底链路。`
