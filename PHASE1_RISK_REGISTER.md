# Phase 1 风险登记

|ID|风险|状态/缓解|
|---|---|---|
|P1-R01|本地健康 API 无认证|仅绑定 `127.0.0.1` 的命令文档；代码没有登录。不得公开部署或作为业务 API|
|P1-R02|没有 Git 根仓库，不能验证提交/ignore/远程CI|已声明；不擅自初始化/推送。正式仓库建立后先检查 `.gitignore` 和运行 Actions|
|P1-R03|真实模型服务数据处理政策未选|Phase 1 无 API Key/供应商依赖；启用前记录供应商、数据范围、条款与预算|
|P1-R04|PostgreSQL、备份、加密和物理删除策略未实现|当前 health 如实显示 `not_configured`；启用持久化前做安全评审|
|P1-R05|API Health schema v1 仍属基础示例|只含非敏感服务状态；新增字段按版本兼容规则同步更新 OpenAPI/Schema/tests|
|P1-R06|异步任务恰好一次/恢复语义尚未建|Phase 1 无任务系统；Phase 3 用 PoC 与故障测试选择机制|
|P1-R07|未来扩展可能误以为平台操作已授权|本阶段无平台适配/账号代码；未来逐项独立审批|
|P1-R08|GitHub Action 依赖上游 action tag|当前按常规 major tag 使用、只读 permissions；仓库治理确认后评估 SHA pinning 策略|
|P1-R09|ruff 在全树检查|`research/`、`.venv*` 和本次 `.phase1-clean-env/` 在项目配置排除；当前检查通过|
|P1-R10|Pydantic Settings 默认忽略未知 `.env` 字段|环境配置文档列明仅支持 `APP_ENV`/`LOG_LEVEL`；未来加入密钥前需明确 secret 管理和字段校验策略|

本表只描述工程底座实际风险，不把未实现的生产组件声称为已安全。
