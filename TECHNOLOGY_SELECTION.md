> AI Content Workforce · G0.1 · 2026-11-24（Asia/Shanghai）
> G0.1 已获批准 · Phase 1 Engineering Foundation V1.0 已实施，待产品负责人验收；未进入 Phase 2。

# MVP 技术选型建议

这是方案选择，不在本轮安装依赖。当前可见开发环境有 Python 3.12、Node 18、Git；这只证明本机工具可用，不等于团队生产标准。建议由Phase1签收后建立单后端栈。

|领域|推荐|优点|缺点/替代|
|---|---|---|---|
|语言/API|Python 3.12 + FastAPI + Pydantic v2|单栈实现Agent/模型/Schema/Worker；类型化API；适合后端AI集成|需团队熟悉Python；替代：若团队强偏TS则全栈TS+Fastify/Nest，避免Python+TS并行|
|数据/队列|PostgreSQL；首版DB-backed jobs/worker polling|事务与运行状态同源，不先引Redis/Broker；可靠恢复可自管小范围|Worker可见性/租约需实现和压测；替代：Redis/Celery或成熟任务队列，只有DB队列瓶颈证据才引入|
|状态执行|固定工作流薄调度模块，先本地PoC评估LangGraph checkpoint|简单链条无需大型编排平台；可针对单worker持久化|恢复/取消边界需自行测；替代：LangGraph在checkpoint收益大于依赖/状态适配成本时采用；n8n不作商业嵌入默认选项，许可见研究|
|Skill格式|内部JSON manifest + JSON Schema 2020-12 + Markdown Prompt|可测试、版本化、外部导出独立|需要实现校验器；Agent Skills标准只作分发适配而非执行权限|
|Artifact|本地文件系统隔离目录+Postgres元数据，storage interface|开发零额外服务；后续映射S3兼容对象存储|单机文件备份/扩展责任；替代：托管S3对象存储，部署阶段决定|
|模型|内部ModelAdapter；开发用FakeAdapter，生产先配置一个团队批准的模型供应商|避免技能绑定SDK和供应商，可做Mock与成本统计|供应商JSON/用量/数据保留能力不同；替代：LiteLLM/官方SDK需单独许可、维护/密钥策略核验，不首轮默认引入|
|UI|先OpenAPI/轻量模板或团队熟悉的现有前端|聚焦工作流与导出，避免强制第三套技术|具体框架未知；建议先定API和最薄可用表单，不把完整SPA列Phase1 |
|测试/协作|pytest、ruff、mypy/pyright择一、Docker Compose仅本地需要时|成熟简明、兼顾接口契约与worker故障测试|额外依赖要锁定；CI由团队仓库选型决定|

## 最小运行基座
单仓库/单后端部署单元，API进程与Worker可作为同镜像不同命令启动；Postgres一个服务；本地Artifact目录。开发可用Docker Compose启动Postgres，但Docker不是业务基础设施前置；不部署Kubernetes、Kafka、Redis、向量数据库、独立对象存储集群或微服务。

## 决策标准
先问团队语言/部署平台、模型数据留存要求、是否单机、文件容量和并发目标。再用一个故障恢复PoC比较自写薄DB队列与LangGraph persistence；按取消、重试和版本修改的真实需求评估。不要以流行度或benchmark单指标选择；如果DB队列简单且透明，先保留；存在并发/延迟瓶颈才演进。

小红书图片生成provider保持接口可空：图像生成服务的商业条款、中文能力、文件存储、内容过滤和成本均待选择。没有服务就只生成Prompt。技术栈最终签收作为Phase1门槛。

## Phase 1 正式决定（2026-11-24）

产品负责人已通过 `ADR/ADR-001-TECH-STACK.md` 正式批准 Phase 1 及未来数据库方向。状态更新如下：

|领域|状态|正式决定/边界|
|---|---|---|
|后端|已确认|Python 3.12、FastAPI、Pydantic v2、Pydantic Settings|
|未来数据库|已确认|PostgreSQL；Phase 1 不连接、不安装服务、不建业务表|
|ORM|当前阶段明确不引入|冻结模型后再评估 SQLAlchemy 2.x + Alembic|
|包管理|已确认|uv、pyproject.toml、uv.lock|
|测试/质量|已确认|pytest、Ruff、mypy；Ruff负责格式和lint|
|CI|已确认|GitHub Actions，PR 和 main push；没有远程时注明未验证|
|前端|Phase 1 明确不做|用户界面交付前再选型|
|Worker/任务|Phase 1 明确不做|不引 Redis、Celery、LangGraph 或 Workflow Engine|
|模型服务|Phase 1 明确不做|全部测试使用本地 Mock，不需要 API Key|
|文件存储|Phase 1 不实现|开发/生产存储和物理删除/备份策略在启用持久化前评审|
|认证|个人本地模式|无公开注册；健康端点不得当作公开业务 API|

本表为 G0.1 建议的版本化补充；未来生产部署、第三方模型、真实文件存储和工作流技术不在此批准范围。
