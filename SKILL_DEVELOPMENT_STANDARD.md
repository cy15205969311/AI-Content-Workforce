> AI Content Workforce / AI 新媒体智能工作台 · V1.1 · 2026-11-24（Asia/Shanghai）
> 状态：研究与设计草案，待产品负责人验收；不构成生产可用或阶段验收证明。

# 统一 Skill 开发规范

本轮只定义内部规范，不创建或安装实际 Skill。支持 prompt/tool/code 三类；V1 优先 prompt 与受控 tool，code 标 disabled。内部 manifest 和外部 SKILL.md 双层适配，不能把项目权限/Schema 塞进某平台专有字段后依赖模型自觉执行。

## 目录和内部契约
```text
skill-id/
  manifest.json
  SKILL.md
  schemas/input.schema.json
  schemas/output.schema.json
  tests/cases.json
  references/provenance.json
  LICENSE
  CHANGELOG.md
```
manifest 必含 skill_id（稳定唯一）、name、description、version（SemVer）、type、category、triggers（含不触发情形）、input_schema、output_schema、permissions、dependencies（固定版本/哈希）、execution_steps、error_policy、test_suite_ref、license、source_refs、research_decision_id、adapter_compatibility、package_hash。许可证/来源不得省略；自研注明内部作者与依据来源。

示例为设计契约，不是可运行 Skill：
```json
{
  "skill_id":"content.title-generator",
  "name":"标题生成器",
  "description":"根据已批准的事实与选题生成候选标题",
  "version":"0.1.0", "type":"prompt", "category":"内容生产",
  "triggers":{"include":["为已选主题生成标题"],"exclude":["发布内容"]},
  "input_schema":"schemas/input.schema.json",
  "output_schema":"schemas/output.schema.json",
  "permissions":[], "dependencies":[],
  "execution_steps":["验证事实引用","生成候选","规则检查"],
  "error_policy":{"missing_input":"INPUT_INVALID","max_attempts":2},
  "test_suite_ref":"tests/cases.json",
  "license":"LicenseRef-Internal-Pending",
  "source_refs":[], "research_decision_id":"required-before-implementation",
  "adapter_compatibility":{}, "package_hash":"computed-at-packaging"
}
```
输入输出使用 JSON Schema 2020-12，顶层 object、明确 required、长度/枚举/数组数量限制、默认 additionalProperties:false；所有跨节点输入用 ArtifactVersion 引用，不能传任意本地路径。业务输出包含 schema_version、content、source_refs、assumptions、warnings；推断与来源事实分离。内部 artifact 引用结构由适配器转换为外部平台所需文件。

## 外部适配
通用 Agent Skills 导出 SKILL.md frontmatter：name 小写 kebab-case、与目录匹配且≤64；description 非空≤1024；可选 license、compatibility≤500、metadata 为 string→string；allowed-tools 若用则为字符串，但实际工具权由运行时决定。版本写 metadata.version，复杂字段放 manifest/schema 文件。兼容性参数化，不照搬旧 quick_validate 白名单或 Remotion 顶层 version。XHS 来源名和内部 ID 映射保留，实际现网打包/加载兼容需要样本验证。

## 流程和版本门禁
需求→生态研究→复用决策→先冻结测试集/业务量表→设计和计划验收→实现→规则/权限/异常/质量/回归→安全许可复核→版本签收→灰度。breaking Schema/权限扩大升 major，新增兼容能力升 minor，修复升 patch；模型、Prompt、工具和模板变化也固定摘要并回归，不修改已发布版本。权限默认空，工具不得通过输入声明而增权。

标准错误：INPUT_INVALID、OUTPUT_INVALID、PERMISSION_DENIED、SOURCE_UNAVAILABLE、MODEL_ERROR、TOOL_TIMEOUT、BUDGET_EXCEEDED、CANCELED。不得自动修复缺失事实为编造；格式修复最多一次且计入预算；安全/权限拒绝不重试。测试样本须在开发前创建、由产品签收，见评估规范。
