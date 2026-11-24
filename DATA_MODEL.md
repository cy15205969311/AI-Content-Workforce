> AI Content Workforce · G0.1 · 2026-11-24（Asia/Shanghai）
> G0.1 已获批准 · Phase 1 Engineering Foundation V1.0 已实施，待产品负责人验收；未进入 Phase 2。



## G0.1 覆写记录（2026-11-24）
本节为当前有效的 Greenfield 版本；上方为保留的 V1.1 历史基线，不再适用的部分已明确标注。完整未改历史快照及 SHA256 见 [research/design-baselines/V1.1/DATA_MODEL.md](research/design-baselines/V1.1/DATA_MODEL.md)。项目状态以 G0.1 为准：没有生产系统待兼容，没有真实小红书账号自动化。

# MVP 数据模型

关系型数据库存业务/执行元数据，文件存Artifact二进制。MVP不需要独立Analytics DB、向量库或全局Skill平台数据库。

|实体|主要字段|
|---|---|
|User/Project/ProjectMember|user_id、project_id、name、role、membership；认证方案未选，不能裸露开发接口|
|ContentRun|run_id、project_id、workflow_id/version、status、revision、input_ref、budget_limit、cost_estimate/actual、model_profile、created_by、timestamps|
|NodeRun|node_run_id、run_id、node_key、attempt、status、input_hash/refs、skill_id/version、model_version、output_artifact_id、usage_json、error_code、lease_until|
|SkillDefinition|skill_id、version、manifest_json、package_hash、enabled、license/source/research refs；MVP可只用源码定义表/静态注册，DB行可后置|
|Artifact|artifact_id、project_id、run_id、node_run_id、kind、version、storage_key、media_type、sha256、schema_version、source_refs、parent_id、stale|
|Approval|approval_id、run_id、revision、package_hash、decision、reviewer_id、decided_at；无外部动作scope|
|UsageRecord|node_run_id、provider/model、input/output tokens nullable、usage_unknown、estimated/actual_cost、currency、pricing_version|
|TaskLease|task_id/run/node、worker_id、lease_until、attempt；若与NodeRun合并需事务保证|

关系：Project 1:N Run；Run 1:N NodeRun/Artifact/Approval；NodeRun 1:N Artifact/UsageRecord。Artifact文件路径以服务端生成opaque key，project_id必须由元数据授权确认。多租户无需立刻全套租户计费，但project_id从首版存在，索引/唯一键/授权一致。

状态：Run queued/running/awaiting_review/succeeded/failed/cancel_requested/canceled；Node pending/running/succeeded/failed/retry_wait/stale。status更新需事务及revision检查。编辑版本不覆盖旧数据；删项目时文件生命周期一并处理并记审计。敏感原始产品资料可设保留期，导出默认去除个人隐私字段。

无需MVP实体：ExternalAction/账号、评论、platform token、复杂全局研究审计、并行DAG checkpoint树、跨租户成本池。为未来添加字段/表不应导致引入这些外部能力。
