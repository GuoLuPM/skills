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

- `codecheck-workflow`
  - 触发：你拿到 CodeCheck、CodeArts Check、静态检查或 lint 导出单，想优先按低风险规则批量收口，而不是大改业务逻辑。
  - 你可以直接说：`先按低风险机械规则分桶处理这份 CodeCheck 导出单，不要主动改业务逻辑。`
