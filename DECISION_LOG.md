



## G0.1 决策纠正（2026-11-24）
|ID|当前决定/状态|取代的历史假设|
|---|---|---|
|G01|项目为Greenfield，从零开发；产品负责人已在本任务书确认|取代D02“现网资产缺失阻断Phase0/Phase1”及 PROJECT_AUDIT.md 的待补现网判断|
|G02|不扫描整机；只使用用户提供路径和工作区现有研究资产|取代任何寻找现网代码的建议|
|G03|XiaohongshuSkills是外部只读参考，不是产品底座或生产接入|保持其独立MIT/安全专题证据|
|G04|MVP为文字工作流、五个Skill、模块化单体+持久单Worker；不要求真实账号/图片服务|取代V1.1复杂分布式引擎及兼容架构提案|
|G05|Global Skill Intelligence Center是研发辅助轻量目录，不是首版用户模块|保留研究政策，推迟自动发现、追踪和审核系统|
|G06|当前等待G0.1产品验收；Phase1尚未授权|取消V1.1路线门槛，但不自动获准开发|

## Phase 1 正式授权记录（2026-11-24）

产品负责人已批准 `ADR/ADR-001-TECH-STACK.md` 中的 Phase 1 选型与范围。该正式授权取代 `PHASE1_TECH_DECISION_REVIEW.md` 的“阻塞等待选型”结论。

|ID|已批准决定|Phase 1 边界|
|---|---|---|
|P1-01|Python 3.12、FastAPI、Pydantic v2、Pydantic Settings|单一后端栈|
|P1-02|PostgreSQL 为未来主关系库|不启动服务、不建立连接或业务表|
|P1-03|不引 ORM|冻结数据模型后另评 SQLAlchemy 2.x + Alembic|
|P1-04|uv、pyproject.toml、uv.lock|锁文件必须纳入交付|
|P1-05|pytest、Ruff、mypy|Ruff 同时执行格式和 lint|
|P1-06|GitHub Actions，PR 与 main push|无远程时只验证本地配置，不擅自建远程|
|P1-07|无独立前端、Worker、Redis/Celery/LangGraph/Workflow/Agent|只建 API 工程|
|P1-08|不配置模型 API；测试使用 mock|不要求真实 key|
|P1-09|本地个人使用，无登录/公开注册/协作|健康路由不能公开部署为业务 API|
|P1-10|资料默认保留至用户主动删除；用户可导出；删项目统一清理|Phase 1 不实现素材存储/删除；生产物理删除与备份策略另审|
|P1-11|UTC ISO-8601、UUIDv4、`/api/v1/`、JSON Schema 2020-12、cursor 预留|Phase 1 只落地 health 和最小版本示例|

原 G0.1 的技术提案仍作为历史背景；冲突时以 P1-01 至 P1-11 正式批准项为准。

## Phase 1 验收记录

实施和 Windows 本地验证材料：`PHASE1_IMPLEMENTATION_REPORT.md`、`PHASE1_TEST_REPORT.md`、`PHASE1_RISK_REGISTER.md`。状态为 waiting for product acceptance；测试通过不自动视为阶段签收，且不授权 Phase 2。

当前 G0.1 设计文档状态横幅已更新为“G0.1 已获批准 / Phase 1 已实施待验收”；V1.1 原始快照保持不变。历史技术阻塞报告已标记为 superseded。
