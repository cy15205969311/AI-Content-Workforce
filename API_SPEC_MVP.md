> AI Content Workforce · G0.1 · 2026-11-24（Asia/Shanghai）
> G0.1 已获批准 · Phase 1 Engineering Foundation V1.0 已实施，待产品负责人验收；未进入 Phase 2。

# MVP API 契约

面向工作台的最小JSON REST API草案；本轮不实现。项目访问先认证，所有 project_id 由服务端核对成员权限。通用错误 `{error:{code,message,retryable},trace_id}`；拒绝越权对象避免泄露。

|方法/路径|语义|
|---|---|
|POST /api/v1/projects|创建项目；是否允许用户注册待决策|
|GET /api/v1/projects/{p}|授权用户读取项目|
|POST /api/v1/projects/{p}/content-runs|提交brief、资料引用、输出数量、style、model profile；202返回run_id|
|GET /api/v1/projects/{p}/runs/{r}|节点状态/输入输出引用/错误/估算和实际用量|
|GET /api/v1/projects/{p}/runs/{r}/events?after={seq}|MVP可轮询增量事件；验证run归属|
|POST /api/v1/projects/{p}/runs/{r}/cancel|记录取消请求，等待在途调用结算|
|POST /api/v1/projects/{p}/runs/{r}/nodes/{n}/retry|失败节点新attempt，检查前置版本一致|
|POST /api/v1/projects/{p}/artifacts/{a}/versions|保存用户中间修改，创建revision并标记依赖后代stale|
|POST /api/v1/projects/{p}/runs/{r}/confirm|确认最终reviewed revision + package_hash；仅表示内容确认|
|GET /api/v1/projects/{p}/runs/{r}/export.md|导出同一确认版本Markdown|
|GET /api/v1/projects/{p}/runs/{r}/export.zip|下载结构化内容包和manifest|

创建示例：`{"topic":"通勤早餐","product_materials":[{"text":"..."}],"target_user":"...","style":"...","output_count":3,"platform_profile":"xiaohongshu-image-text@1","model_profile":"default"}`。响应包含 `{run_id,status,revision,trace_id}`。token预算和速率由服务端限制，客户端不能指定最大支出以上的模型调用参数。

Idempotency-Key用于创建run/取消/确认；artifact编辑用If-Match revision。401未认证、403无权、404未知/无权、409revision冲突、422输入Schema错误、429任务/预算限制、503模型服务暂时失败。明确错误：MISSING_REQUIRED_INPUT、MODEL_NOT_CONFIGURED、OUTPUT_INVALID、BUDGET_EXCEEDED、APPROVAL_STALE、RUN_CANCELED。没有 platform login/publish/comment/search API。
