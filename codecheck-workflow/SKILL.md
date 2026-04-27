---
name: codecheck-workflow
description: 只有当用户明确说“华为 CodeCheck”“CodeArts Check”“华为云代码检查”，或给出华为 CodeArts Check 规则名、导出单时才使用。适用于华为 CodeArts Check 的 `.xlsx` 缺陷导出、规则分桶、规则名解释、低风险规则批量收口、方法顺序重排和整改闭环验证。不适用于日常写代码、业务逻辑改动、代码重构、架构重构、测试失败排障或任何会改变语义与返回契约的任务。
---

# CodeCheck 工作流

## 核心边界

CodeCheck 只处理代码表达形式问题。

它不是：

- 业务逻辑改造
- 代码重构
- 架构重构

默认原则：

- 不主动改业务逻辑
- 不借规范整改顺手整理实现
- 不为了过门禁去改调用链、异常语义、状态语义或返回契约

## 什么时候用

- 用户明确提到华为云 `CodeArts Check`、`CodeCheck`、华为代码检查。
- 用户给出华为规则名，如 `G.CLS.06`、`G.FMT.02`、`G.CLS.11`。
- 用户给的是华为这套门禁导出的 `.xlsx`、`.csv`、文本报告、规则列表、问题列表。
- 用户明确说的是“帮我处理华为 CodeCheck”，而不是一般性的代码问题。

## 不适用

- 普通写代码、日常编码辅助。
- 没有明确出现“华为 CodeCheck / CodeArts Check / 华为云代码检查”的质量问题。
- 用户要做业务功能改造。
- 用户要求借机做代码重构或架构重构。
- 问题已经明确落在异常语义、fallback、缓存兼容、状态恢复、返回契约上。

## 先做的事

1. 先识别这是不是华为 `CodeArts Check` 语境。
2. 如果问题名里出现 `G.*` 前缀，或者用户明确提到华为云代码检查，先读 `references/huawei-codearts-check.md`。
3. 如果用户问的是产品/API/任务配置，而不是代码整改，也先读 `references/huawei-codearts-check.md`，优先使用官方文档，不要把样例脚本当标准。

## 快速流程

1. 先确认输入是什么：原始导出单、归一化问题项，还是人工整理后的规则列表。
2. 如果输入是 `.xlsx`，优先运行 `scripts/summarize_codecheck_xlsx.py` 先做规则/文件分布统计。
3. 按性质把规则分两桶：
   - 表达形式桶：文件头、docstring、长行、未使用导入、注释废代码、`staticmethod`、纯方法顺序重排、JS 字面量/声明/嵌套三元表达式等语法表达问题。
   - 非表达形式桶：任何会引出结构整理、语义变化、异常路径变化、状态变化、返回契约变化的问题。
4. 只处理表达形式桶，不混入非表达形式规则。
5. 对 `G.CLS.06 / function-order` 这类规则，也只允许做纯方法顺序重排，不允许顺手整理实现。
6. 多轮导出单之间可能互相冲突；以当前轮导出单为准，旧表只能做背景参考。
7. 对每一批改动做固定验证，不要因为是“规范问题”就省掉验证。

## 华为 CodeArts Check 模式

如果当前输入是华为这套门禁，默认采用下面的知识优先级：

1. 当前代码和当前工作树状态
2. 当前轮导出单
3. 同任务历史导出单
4. 华为云官方 `CodeArts Check` 文档和 API 文档
5. Jenkins / Gitee / 第三方接入样例

不要默认代理已经理解华为规则前缀。需要时先读参考文档里的规则族解释，再做分桶。

## 固定验证闭环

- `python -m py_compile <files>`
- `git diff --check -- <files>`
- 关键模块最小 import smoke
- 长行扫描
- 对 `G.CLS.06`，额外验证当前导出单中的 `A should be after B` 关系为 0 失败。
- 对方法重排，额外用 AST hash 对比方法体和装饰器，确认只移动方法块。
- 对 JS/ECMAScript 表达式规则，额外做解析/语法/规则反扫：Babel parse、`node --check <files>`、`git diff --check`，并确认“已修改文件集合”和“当前导出单文件集合”一致。

如果是多文件批次：

- 对所有已改 Python 文件做 `py_compile`
- `git diff --check -- '*.py'`
- 对所有已改 JS 文件做 `node --check`

## 默认可直接推进的规则

- `C0116`
- 文件头规则
- 行宽
- 未使用导入
- 注释废代码
- `staticmethod / classmethod`
- `G.CLS.06`
- 基础缩进和空格规则
- JS 低风险表达规则：`G.DCL.01` (`var` -> `let/const`)、`G.DCL.03`（每条语句一个声明）、`G.DCL.06`（`new Object/Array` 字面量）、`G.TYP.01`（`.08` -> `0.08`）、`G.EXP.03`（嵌套三元改为等价 `if/return` 表达式）。

## 默认只记录风险、不自动推进的规则

- `G.CLS.11`
- `G.LOG.02`
- `G.ERR.07`
- `G.ERR.11`
- 任何需要抽 helper、拆函数、整理控制流才能过的规则
- 返回值统一但会改返回契约的规则
- `shell=True / shell=False`
- JS `alert` 替换：只有项目已有等价通知入口（如 `setStatus`、toast、message）且周边代码同样使用时才可直接改；否则先标风险，因为 `alert` 的阻塞弹窗语义和普通状态提示不同。
- fallback、默认值补偿、cache bypass
- session / runtime state / history restore 相关语义调整

## 输出要求

无论是分析还是整改建议，输出至少包含：

- 当前优先级最高的规则桶
- 哪些问题适合纯表达形式处理
- 哪些问题已超出表达形式边界
- 当前建议的执行顺序
- `[假设]`
- 证据

如果用户问的是华为平台本身，而不是具体代码整改，输出还要包含：

- 使用了哪份官方文档
- 这是产品事实、样例做法，还是当前代码状态

## 停手条件

- 需要改变返回结构。
- 需要改变异常传播。
- 需要改变 fallback / cache / session / history 语义。
- 需要抽 helper、拆函数、整理控制流才能过规则。
- 需要跨多个模块同步重构才能过规则。

出现这些情况时，应改为“列风险 + 等用户确认”，不要继续自动整改。

## 需要时再读

- 需要更完整的方法论、风险分桶、验证建议、多轮报告冲突处理、JS 批量机械整改、`G.CLS.06` 拓扑重排经验时，读 `references/playbook.md`。
- 需要解释华为 `CodeArts Check`、规则族、资料来源、任务配置、API 或最佳实践时，读 `references/huawei-codearts-check.md`。
- 需要快速统计 `.xlsx` 导出单时，运行 `scripts/summarize_codecheck_xlsx.py`。
