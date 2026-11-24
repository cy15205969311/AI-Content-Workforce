# Phase 1 测试报告

日期：2026-11-24 · Windows PowerShell · Python 3.12.10 · uv 0.11.7。
项目根目录此前不是 Git 仓库；所以实际 `.gitignore` 判断、GitHub Actions 托管运行和 PR 分支触发未能执行。

## 干净依赖安装

创建隔离目录 `.phase1-clean-env` 作为全新项目环境，设置 `UV_PROJECT_ENVIRONMENT` 后执行 `uv sync --locked --default-index https://pypi.org/simple/ --all-groups`。34 个锁定包从空环境安装成功，应用包可导入；在这个全新环境内 Ruff、mypy 和全部 13 项测试也通过。随后在主 `.venv` 执行完整依赖重装复核。`uv lock --check --default-index https://pypi.org/simple/` 成功。锁文件使用 Python 3.12、公开 PyPI 和哈希，不含开发者环境中配置的私有镜像地址。uv 在 Windows 文件系统间不能使用硬链接时回退为复制，属于性能提示，未影响安装。`.phase1-clean-env` 是本次验证用本地环境，已列入 `.gitignore`。

## 本地检查

|检查|结果|实际结果|
|---|---|---|
|Ruff lint|PASS|`uv run --locked --default-index https://pypi.org/simple/ ruff check .` — All checks passed|
|Ruff format|PASS|`uv run --locked --default-index https://pypi.org/simple/ ruff format --check .` — 63 files already formatted|
|mypy|PASS|`uv run --locked --default-index https://pypi.org/simple/ mypy src/` — Success, no issues in 8 source files|
|pytest|PASS|`uv run --locked --default-index https://pypi.org/simple/ pytest` — 13 passed|
|依赖锁一致性|PASS|`uv lock --check --default-index https://pypi.org/simple/` — 34 packages resolved, lock unchanged|
|JSON Schema 文件|PASS|两个 schema 文件均通过 Python JSON parser；测试也确认 2020-12 标记和版本字段|
|CI YAML 语法|PASS (本地解析)|PyYAML BaseLoader 可解析 workflow 为 mapping；未由 GitHub Actions 运行|
|密钥忽略规则|PASS (静态)|`.gitignore` 包含 `.env`、`.env.*` 和 `!.env.example`；没有实际 `.env`。Git 本地追踪/ignore 状态因无 `.git` 目录无法验证|

## 真实服务 smoke check

在 Windows 启动 `uv run --locked --default-index https://pypi.org/simple/ uvicorn ai_content_workforce.main:app --host 127.0.0.1 --port 8765 --no-access-log` 后，通过 PowerShell HTTP 请求实际验证：

- `/health`: `status=ok`、`version=1.0.0`、`environment=development`、`database.status=not_configured`。
- `/api/v1/health`: 返回相同 liveness 合同。
- `/api/v1/`: 返回 `api_version=v1`、`schema_version=1.0`。
- 服务成功启动并正常停止；日志只有白名单事件、request ID、方法和状态码。

自动化测试覆盖配置默认值/环境变量/错误值脱敏、两条健康路径、API 版本、404 和 422 统一错误、数据库未配置、健康内容字段、意外异常不泄漏到日志/响应、Schema文件和 `.env` 规则。未访问网络模型、数据库、小红书账号或图片服务。

## 未验证项

GitHub remote 不存在，故真实托管 CI 为 **NOT VERIFIED**。没有 Git 元数据，不能证明文件已提交或由 Git 正确忽略。PostgreSQL 没有配置/启动/连接；production deployment/公开网络暴露/认证、备份、加密、物理删除和生产数据管理均不属于 Phase 1。虽然已添加 CI 文件，仍需在未来关联 GitHub 仓库后验证 Action 版本、主分支和托管运行结果。
