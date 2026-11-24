# Coding standards

- Target Python 3.12; use type annotations for application functions.
- Keep HTTP handlers small and move reusable infrastructure into `core/` only
  when it has a real Phase 1 use.
- Validate external input through Pydantic/FastAPI; do not log request bodies,
  query values, credentials, exception text, or local private paths.
- Return stable snake_case JSON fields. Use `schema_version` for response
  schemas and explicit, stable error codes.
- Use UTC ISO-8601 for timestamps and UUIDv4 for generated identifiers.
- Keep project/user material out of health endpoints and logs.
- Do not add database, model, browser, or workflow integrations to the Phase 1
  skeleton.
- Ruff owns formatting and lint. Mypy checks `src/`; pytest owns automated tests.
- Pin every dependency through `uv.lock`; update the lock in the same change as
  `pyproject.toml`.

Before submitting a change, run `uv run --locked ruff format --check .`,
`uv run --locked ruff check .`, `uv run --locked mypy src/`, and
`uv run --locked pytest`.
