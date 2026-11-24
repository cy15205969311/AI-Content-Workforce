> AI Content Workforce · G0.1 · 2026-11-24（Asia/Shanghai）
> G0.1 已获批准 · Phase 1 Engineering Foundation V1.0 已实施，待产品负责人验收；未进入 Phase 2。

# Skill Registry 与 Runtime（MVP）

## 目录和manifest
每个Skill以单独目录/模块登记，但第一版和产品同仓、同版本打包，不允许运行时自动扫描并执行外部仓库。

```text
skills/
  product-analyst/{manifest.json,prompt.md,schemas.json}
  audience-needs/{manifest.json,prompt.md,schemas.json}
  topic-generator/{manifest.json,prompt.md,schemas.json}
  xhs-copywriter/{manifest.json,prompt.md,schemas.json}
  visual-editor/{manifest.json,prompt.md,schemas.json}
```
manifest必含skill_id、name、description、version、type、category、trigger include/exclude、input/output Schema、permission scopes、fixed dependencies、execution steps、error policy、tests、license/source、research decision、package hash。自研许可明确写内部权属，不使用占位LicenseRef冒充最终许可。

首版类型：PromptSkill向ModelAdapter发送受限上下文；ToolSkill仅为内部白名单纯函数/格式化和规则校验。Code Skill、shell、动态依赖、MCP任意服务器、浏览器均禁用。skill 版本和prompt hash固定进run。

## 执行管线
Registry解析已登记定义 → 认证ProjectContext → 验证输入 Schema → 校验capability allowlist与预算 → 拼装最小上下文/提示 → ModelAdapter调用 → 将文本按严格输出Schema解析 → 确定性规则检查 → Artifact写入 → 记录版本/耗时/用量/错误。工具权限不靠Prompt声明；节点不能从模型输出选任意工具。

## 接口
`resolve(skill_id, version) -> SkillDefinition`; `validate_input(definition, json) -> ValidationResult`; `execute(definition, input, restricted_context, run_context) -> SkillExecutionResult`; `validate_output(...)`; `record_evaluation(...)`。报错OUTPUT_INVALID、INPUT_INVALID、PERMISSION_DENIED、MODEL_UNAVAILABLE、MODEL_TIMEOUT、BUDGET_EXCEEDED、CANCELED。Prompt响应结构不合法只允许有限一次格式修复且花费纳入预算。

## 核心数据
SkillDefinition：id/name/description/version/type/category/triggers/schemas/permissions/dependencies/error_policy/tests/license/source_ref/hash. SkillExecution：run_id/node_id/attempt_id、input_hash、skill_version、model_version、prompt_hash、started/ended、token_usage或unknown、cost estimate/actual、status/error、artifact refs。

## 评估约束
每个Skill先建覆盖正常、缺参、极端、格式、异常、权限、业务质量、回归的固定小测试集；先用mock验证契约和规则，模型业务评估之后逐个做。首批上架需Schema与权限硬门禁全过、重大事实错误为0、内容评审通过；具体阈值在验收文件由产品签收。

外部 Agent Skills 格式仅用导出适配器呈现；依据登记的研究与许可证手工审核，绝不自动安装或因兼容SKILL.md就信任执行。
