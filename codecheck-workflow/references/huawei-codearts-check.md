# 华为 CodeArts Check 说明

## 适用时机

只有在下面场景才需要读这份参考：

- 用户明确提到华为云 `CodeArts Check` / `CodeCheck`
- 规则名带华为风格前缀，例如 `G.CLS.06`、`G.FMT.02`
- 用户问产品能力、任务配置、API、MR 增量检查、私有码扫描、Jenkins 集成

## 一条总原则

处理华为这套门禁时，不要假设代理天生知道它的规则命名和产品边界。

先区分三件事：

1. 产品事实：来自官方文档或 API 文档
2. 当前代码事实：来自当前仓库
3. 接入样例：来自 Jenkins、Gitee、脚本仓

样例只能解释“别人怎么接”，不能代替产品契约。

## 产品定位

按华为云官方用户指南，`CodeArts Check` 是一个云端代码检查服务，覆盖代码风格、通用质量和安全风险，并提供检查报告、问题处理和质量门禁等能力。

官方用户指南入口：

- Working with CodeArts Check
  - https://support.huaweicloud.com/intl/en-us/usermanual-codecheck/codecheck_01_1002.html

## 最常用的官方资料来源

### 用户指南和任务配置

- Working with CodeArts Check
  - https://support.huaweicloud.com/intl/en-us/usermanual-codecheck/codecheck_01_1002.html
- Creating a Task
  - https://support.huaweicloud.com/intl/en-us/usermanual-codecheck/codecheck_ug_0000.html
- Configuring Check Scope
  - https://support.huaweicloud.com/intl/en-us/usermanual-codecheck/codecheck_01_0022.html
- Configuring Quality Gates
  - https://support.huaweicloud.com/intl/en-us/usermanual-codecheck/codecheck_01_1004.html
- Configuring a Custom Rule Set
  - https://support.huaweicloud.com/intl/en-us/usermanual-codecheck/codecheck_01_0009.html
- Configuring a Custom Environment
  - https://support.huaweicloud.com/intl/en-us/usermanual-codecheck/codeartscheck_01_7033.html
- IntelliJ IDEA plug-in
  - https://support.huaweicloud.com/intl/en-us/usermanual-codecheck/codecheck_ref_0001.html

### API

- API Reference Description
  - https://support.huaweicloud.com/intl/es-us/api-codecheck/codecheck_03_0005.html

如果用户问“怎么自动化创建任务、执行检查、查 issue、拉日志”，优先从 API 文档回答，不要引用第三方脚本当标准。

### 最佳实践

- 通过 API 执行 MR 增量检查
  - https://support.huaweicloud.com/bestpractice-codecheck/codeartscheck_14_1009.html
- 不上传代码到云服务的情况下使用代码检查
  - https://support.huaweicloud.com/bestpractice-codecheck/codeartscheck_14_1008.html
- 使用自定义执行机执行代码检查任务
  - https://support.huaweicloud.com/bestpractice-codecheck/codeartscheck_14_1007.html
- 使用 Jenkins 插件集成 CodeArts Check
  - https://support.huaweicloud.com/bestpractice-codecheck/codeartscheck_14_1010.html

## 规则族的常见理解方式

这些不是完整规则定义，而是做分桶时最常用的经验分类。

### `G.CMT.*`

注释、文件头、版权声明相关。

### `G.FMT.*`

格式、缩进、空格、行宽、导入位置相关。

### `G.CLS.*`

类、方法顺序、`staticmethod/classmethod`、受保护成员访问相关。

其中：

- `G.CLS.06` 往往可以通过纯方法重排处理。
- `G.CLS.11` 很容易触碰语义边界，默认进风险桶。

### `G.CTL.*`

控制流、返回分支一致性、条件复杂度相关。

### `G.ERR.*`

异常处理、错误传播、`SystemExit`、忽略异常等。

### `G.FNM.*`

函数接口、返回值、参数组织相关。

### `G.LOG.*`

日志记录方式相关。

### `G.EXP.*`

lambda、推导式、表达式复杂度相关。

### `R0914` / `huge_cca_cyclomatic_complexity`

通常来自 pylint / cmetrics 这一类工具，属于“结构问题”，不是简单格式问题。

## 推荐回答策略

### 用户问产品知识

先引用官方文档，再补你的解释。

### 用户问这份导出单怎么处理

先看当前代码和当前导出单，再用规则族做风险分桶。

### 用户问某条规则能不能直接改

先判断它属于：

- 机械规则
- 结构规则
- 语义风险规则

不要只看规则名就给肯定答案。

## 不该做的事

- 不要把 Jenkins 或 Gitee 样例当作 API 契约。
- 不要把旧导出单当成当前事实。
- 不要因为规则前缀看起来统一，就假设风险等级统一。
- 不要默认所有 `G.*` 规则都能“只改风格”解决。
