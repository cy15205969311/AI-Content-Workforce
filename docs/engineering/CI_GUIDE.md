# CI guide

`.github/workflows/ci.yml` runs on pull requests and pushes to `main` using
GitHub Actions. It grants read-only repository permissions, installs Python
3.12 and uv, syncs the committed lock with `--locked` and the public PyPI
index, and runs Ruff format, Ruff lint, mypy, and pytest. There are no required
secrets or service containers.

The workflow file is present and statically reviewed locally. This directory
was not a Git repository and has no configured GitHub remote during Phase 1,
so a remote Actions run is **not verified**. Do not create or push a remote
repository without separate authorization.

GitHub接入补充（2026-11-24）：本地Git现已初始化，origin指向指定正式仓库；此前“非Git仓库”仅为Phase1历史。提交与push尚未批准，远程refs网络检查未成功，因此Actions仍未验证。当前状态详见根目录 GITHUB_INTEGRATION_REPORT.md。
