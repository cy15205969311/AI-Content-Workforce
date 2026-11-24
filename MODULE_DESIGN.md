> AI Content Workforce · G0.1 · 2026-11-24（Asia/Shanghai）
> G0.1 已获批准 · Phase 1 Engineering Foundation V1.0 已实施，待产品负责人验收；未进入 Phase 2。



## G0.1 覆写记录（2026-11-24）
本节为当前有效的 Greenfield 版本；上方为保留的 V1.1 历史基线，不再适用的部分已明确标注。完整未改历史快照及 SHA256 见 [research/design-baselines/V1.1/MODULE_DESIGN.md](research/design-baselines/V1.1/MODULE_DESIGN.md)。项目状态以 G0.1 为准：没有生产系统待兼容，没有真实小红书账号自动化。

# 核心模块职责与契约

MVP运行形态是一个代码库内的模块边界，而非十个部署单元。下表的API为模块调用契约草案；外部HTTP只暴露必要的项目/run/artifact/approval端点。

|模块|职责/输入→输出|依赖|MVP|
|---|---|---|---|
|Project Management|用户授权上下文+项目成员→Project/AccessDecision|API、DB|必须；单用户也保持project_id界限|
|Skill Registry|内部manifest、version/hash→已知SkillDefinition|Schema校验|必须但仅静态目录/代码注册；无在线市场|
|Skill Runtime|skill_id/version、独立JSON input→Schema验证后的JSON output|ModelAdapter、Registry、质量规则|必须；Prompt与受控函数，不任意Code Skill|
|Workflow Engine|workflow version、input artifact refs→节点状态/最终内容包|DB、Skill Runtime、Artifact|必须；固定顺序DAG、失败恢复；首版不需通用可视化编排器|
|Agent Orchestrator|自然语言brief→ValidatedBrief、workflow选择/补问|Project Management、Workflow目录|轻量必须；固定路由，不自主生成/执行DAG|
|Context Manager|项目Profile和显式artifact refs→节点最小上下文|项目权限、Artifact|必须；显式传递，无隐式全历史/向量数据库|
|Artifact Manager|项目、类型、内容、来源→不可变ArtifactVersion/ref|本地目录/对象存储、DB|必须；版本/哈希/导出|
|Quality Engine|输出+Schema+规则→问题/阻断状态|Skill/平台Profile|必须；确定性规则+人工检查，不需单独质量微服务|
|Approval Manager|最终包hash+审核者decision→有效/失效记录|Project、Artifact|必须；MVP一处内容确认，不做多级审批编排|
|Model Adapter|标准请求/模型版本/预算→标准文本/JSON/usage/error|供应商SDK/HTTP|必须；先一个配置供应商+mock接口；不绑定Skill|

## 输入/输出/错误
Skill统一 `execute(input: JSON, context: RestrictedContext) -> SkillResult`；SkillResult包含schema_version、data、source_refs、assumptions、warnings、usage。跨模块失败使用 Error(code,retryable,message,trace_id,details redacted)。权限拒绝/Schema错误不可重试；供应商暂时错误有限重试；预算超限终止。模块不可写其他项目Artifact。

## API边界
必要HTTP：POST /projects/{p}/content-runs、GET /projects/{p}/runs/{r}、GET /projects/{p}/runs/{r}/events（初期轮询可代替SSE）、POST /projects/{p}/runs/{r}/cancel、POST /projects/{p}/artifacts/{a}/versions（中间编辑）、GET /projects/{p}/artifacts/{a}/versions/{v}、POST /projects/{p}/runs/{r}/confirm、GET /projects/{p}/runs/{r}/export.md。Skill Registry/Context/Quality走内部接口。外部平台动作API不存在于MVP。

## 错误/不实现
Artifact 不存在/项目不符统一拒绝；Context不自动从其他项目、全网或全部历史召回；模型Adapter provider故障映射MODEL_UNAVAILABLE；输出JSON无法修复则OUTPUT_INVALID，不靠无界重新prompt。首版不做Skill安装市场、MCP任意连接、审计门户、向量检索、完整LLM Agent工具循环。
