# Development guide

Requirements: Python 3.12 and uv. The project was verified with Python 3.12.10
and uv 0.11.7 on Windows PowerShell. `uv.lock` pins the resolved dependency
set. Commands explicitly select public PyPI so a developer's private/mirror
`UV_DEFAULT_INDEX` cannot silently change lock resolution or installation.

From the project root:

```powershell
uv sync --locked --default-index https://pypi.org/simple/ --all-groups
uv run --locked --default-index https://pypi.org/simple/ uvicorn ai_content_workforce.main:app --host 127.0.0.1 --port 8000 --no-access-log
```

`--no-access-log` avoids emitting URL paths and query strings into server logs.
The local API docs are at `/api/v1/docs`; liveness is available at `/health`
and `/api/v1/health`. The Phase 1 service binds to loopback by default in the
documented command and has no authentication, so do not expose it publicly.

Run checks with the commands in `TESTING_STRATEGY.md`. No database, model key,
image service, or Xiaohongshu account is required. `.env` is optional and read
from the project root; never commit it.
