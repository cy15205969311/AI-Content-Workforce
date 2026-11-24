# Phase 1 技术决策审查

项目：AI Content Workforce · V1.0 / Phase 1 · 2026-11-24
审查范围：只核对 G0.1 提案和待决项；不创建工程文件、不安装依赖、不连接服务。
状态：**已被正式授权书取代；仅作为历史决策审查留档。**

2026-11-24 产品负责人提交《Phase 1 正式实施授权书》并批准核心选型。当前批准范围见 [ADR-001-TECH-STACK.md](ADR/ADR-001-TECH-STACK.md)。

> 历史状态：本报告编写时尚未收到正式技术授权。2026-11-24 产品负责人随后提交《Phase 1 正式实施授权书》，该等待状态已被正式决策取代；当前技术依据和批准范围见 [ADR/ADR-001-TECH-STACK.md](ADR/ADR-001-TECH-STACK.md)。

## 审查结论

G0.1 文档提出了方向，但没有记录产品负责人对核心技术栈的明确批准。`TECHNOLOGY_SELECTION.md` 将 Python/FastAPI、PostgreSQL、DB-backed worker、静态 Skill manifest、文件存储、Mock/模型适配器、pytest/ruff 等标为建议；`OPEN_DECISIONS.md` 的 O04、O05、O06、O07、O10、O11（技术栈、模型和数据处理、文件策略、用户边界、Artifact部署、工作流执行）仍待确认。G0.1 主 README 和阶段状态也仍写“等待确认”。本轮 Phase 1 任务书授权准备工程底座，但要求这些决策先得到确认，因此暂不创建应用骨架。

## 选项审查

|领域|当前状态|建议|替代方案、理由与成本|
|---|---|---|---|
|后端语言/API|**已推荐，未确认**：Python 3.12 + FastAPI|若团队可维护 Python，采用 Python 3.12、FastAPI、Pydantic v2；Phase 1 仅启动入口、配置、健康检查和错误响应|替代 TypeScript + Fastify/NestJS。单一后端语言更省维护；TypeScript 只有在团队经验/现有工具链明显更强时更划算。两者都需锁定依赖和维护运行时。当前主机能找到 Python 3.12、Node 18 只说明工具可用，不能代表团队偏好。|
|前端|**尚未决定**|Phase 1 不建立独立前端；以 OpenAPI/健康端点作为工程骨架。MVP 用户工作台前端在后续阶段按团队栈确定|React/Next.js、Vue 等会增加 Node 构建、依赖和部署面；Phase 1 验收不要求完整 UI。若产品要求本阶段交付可交互 UI，需另确认框架与范围。|
|数据库|**已推荐，未确认**：PostgreSQL|PostgreSQL 作为未来项目/运行元数据的主关系库；Phase 1 可不启用真实连接，健康接口应返回 database=not_configured，而不是伪报健康|SQLite 可降低个人本地试运行门槛，但并发任务、事务领取和后续部署语义不同；不建议把 SQLite 生产化后再迁移。Postgres 增加本地/部署服务、备份和升级成本。任务书中产品资料保留期/删除策略还未定，启用持久化前需要负责人确认。|
|ORM|**尚未决定**|若 Phase 1 只做健康服务，先不引 ORM。Phase 3 冻结数据模型后，在 PostgreSQL 已批准前提下评估 SQLAlchemy 2.x + Alembic|SQLModel API 更简洁但仍需理解 SQLAlchemy；原生 SQL 最少抽象但 schema 迁移、事务和类型约束需自管。现在选择 ORM 不会帮助 Phase 1 健康检查。|
|任务执行机制|**已推荐，未确认**：数据库任务记录 + 单 Worker polling；未批准代码实现|Phase 1 不建 Worker/队列。Phase 3 用短 PoC 评估 Postgres job 表/租约与获批持久工作流库，再选 MVP 机制|DB polling 少一个 Redis/消息代理，运维轻，但租约、重复投递、崩溃恢复要测试。LangGraph 有 checkpoint/interrupt 能力但会增加框架和状态适配；n8n 许可证和嵌入方式不适合作默认内核。Kafka、Celery/Redis、微服务均超出当前必要范围。|
|测试|**已推荐，未确认**：pytest|若采用 Python，批准 pytest + FastAPI TestClient/httpx 的纯本地测试；CI 使用 mock，不需数据库或模型 Key|unittest 无外部框架但 fixture/插件生态较少。采用 TypeScript 时改用其单一生态测试框架，不并列安装 Python 测试工具。|
|格式/静态/类型工具|**已推荐，未确认**：ruff 与 mypy/pyright择一|Python 建议 Ruff（lint/format）+ mypy；只选一个类型检查器|Pyright 对编辑器/快速类型检查体验较好；mypy 配置广泛。Ruff 类型检查能力不能替代成熟类型检查器。工具数量保持最少。|
|包管理与锁文件|**尚未决定**|Python 栈建议 uv 管理 `pyproject.toml` 和提交 `uv.lock`；CI 使用锁定同步安装|Poetry 项目管理成熟但工具配置较多；pip-tools 直接但开发工作流组件少；pip+宽松 requirements 不满足可复现锁定要求。选型后需在干净环境验证锁文件。|
|配置读取|**尚未决定**|若采用 FastAPI/Pydantic，选 Pydantic Settings；环境变量集中加载、启动时 fail-fast，health 输出不得回显值|标准库自行解析环境变量可减少依赖，但需要自写类型、默认值和错误定位。不能提交 `.env`。|
|CI|GitHub Actions 平台**由 Phase 1 任务明确指定**；workflow细节未定|单一 workflow 在 PR 和主开发分支 push 触发；锁定 Python、安装锁文件、format/lint/type/test；只用 Mock，无 secret|其他 CI 不符合本阶段明确的 GitHub Actions 要求。需仓库默认分支/权限配置后验证真实运行；本地检查成功不等于 CI 实际运行通过。|
|文件存储|本地开发文件目录为**已推荐、未确认**；生产对象存储未定|Phase 1 不处理用户上传；后续开发先用项目隔离的本地 Artifact 存储抽象。生产环境目标和删除/备份由负责人确定后再配置对象存储|S3 兼容服务适合部署但产生供应商、密钥、生命周期/备份成本。不能仅凭接口抽象就宣称文件安全或数据处理决策已完成。|
|API与 Schema 版本|`/api/v1/` 与 Schema 有版本字段为**需求已明确**；具体契约仍为提案|维持 URL major version `/api/v1`；JSON Schema 2020-12；响应/错误结构由项目标准冻结；Schema示例显式 `schema_version: "1.0"`|按破坏性API变更升 major 或有迁移；Schema增加兼容字段也不得静默改变语义。版本字符串的增量/废弃策略仍需技术负责人写进规范。|
|认证/项目成员|**尚未决定**|Phase 1 不做公开注册或假认证；健康端点无用户数据。首个业务写API前必须决定用户身份、单用户/多项目及隔离方式|单用户本地部署减少系统面；多用户托管需要可靠认证、成员授权、审计和密钥策略。当前文档仅说保留 project boundary，不能视为已选身份方案。|
|时间、ID、分页、日志|**部分已推荐，待写入规范**：UTC/UUID/cursor|规范时间 UTC ISO-8601、显示层本地化；UUID；不暴露 secret 的结构化日志；分页 cursor|G0.1 文档没有统一选定 UUID具体版本，也没有确定 cursor 编码。Phase 1 可写标准并给 health 示例，但业务API分页实现应后置。|

## 推荐栈与维护/部署评估

若产品负责人确认团队采用 Python，建议 MVP 的最小生产栈为：Python 3.12、FastAPI、Pydantic v2/Pydantic Settings、PostgreSQL（到需要业务持久化的阶段启用）、SQLAlchemy 2.x + Alembic（Phase 3 再引入）、uv + `uv.lock`、pytest、Ruff、mypy、GitHub Actions、开发期本地 Artifact 目录。Phase 1 健康骨架可只需要 Python、API框架、配置、测试/质量工具和 CI，不需要 PostgreSQL 连接、ORM、前端、任务框架或模型供应商。

优点是一个后端语言、Python AI 生态直接、类型化请求/Schema清晰、CI和开发基座无需外部模型。主要维护成本在异步Worker/数据库事务成熟前不可过早自建；部署复杂度低至中（应用进程，后续才加 PostgreSQL 和对象存储）。团队技术熟练度未知，是关键不确定性。Node/TypeScript 替代栈同样可行；依据目前资料无法证明它比 Python 更符合团队实际。

## 需产品负责人确认

请明确以下决定，才可执行 Phase 1：

1. 是否批准 Python 3.12 + FastAPI/Pydantic v2 为后端基础栈，或指定 TypeScript/其他团队主栈？
2. 是否批准 PostgreSQL 作为未来主业务数据库？本阶段暂不接入数据库。产品资料及生成内容的保留、导出和删除要求由谁确认？
3. 是否同意 Phase 1 暂不建前端、不建 ORM/Worker/工作流依赖；这些分别推迟到有需求的阶段？
4. 若选 Python，是否批准 `uv`、pytest、Ruff、mypy，并提交 `uv.lock`？
5. GitHub Actions 使用的主开发分支名称是什么？（可在仓库建立后配置，不影响栈批准，但影响CI触发验证。）

推荐回复格式：`后端栈：Python/FastAPI`；`数据库：PostgreSQL/其他`；`uv + pytest + Ruff + mypy：批准/调整`；`Phase 1 不建前端/ORM/Worker：批准/调整`；`CI主分支：<名称>`；`数据保留要求负责人/原则：<内容>`。

## 停止点

在以上核心决策明确之前，本轮不建立代码目录、依赖清单/锁文件、应用骨架、CI workflow 或数据库配置；也不虚构任何数据库连接状态。产品负责人回复批准后，Phase 1 实施再从项目结构和最小应用骨架开始。本报告不代表 Phase 1 已验收。
