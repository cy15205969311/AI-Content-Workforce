# Testing strategy

Tests are local and deterministic; they require no external model, database,
image provider, account, or network access.

- `tests/unit/`: configuration validation and pure application behavior.
- `tests/integration/`: in-process ASGI requests for routes, responses, errors,
  database status, and sensitive-output boundaries.
- `tests/fixtures/`: add only when shared fixtures are actually needed.

Current checks:

```powershell
uv run --locked --default-index https://pypi.org/simple/ ruff format --check .
uv run --locked --default-index https://pypi.org/simple/ ruff check .
uv run --locked --default-index https://pypi.org/simple/ mypy src/
uv run --locked --default-index https://pypi.org/simple/ pytest
```

Coverage is a diagnostic, not a release gate in this phase. Every new route
should test its successful response and relevant safe failure response. Tests
must not connect to PostgreSQL: `database.status` must remain
`not_configured`. A future database phase will define isolated test storage
before adding integration tests that use it.
