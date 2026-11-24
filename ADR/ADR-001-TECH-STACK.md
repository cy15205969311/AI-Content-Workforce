# ADR-001: Phase 1 engineering technology stack

- Status: Accepted by product owner on 2026-11-24
- Decision scope: Phase 1 Engineering Foundation; does not authorize later
  database, model, frontend, worker, or workflow implementation

## Context

AI Content Workforce is a Greenfield project. Phase 1 needs a small backend
foundation that starts locally, validates settings, serves safe health/API
version endpoints, and runs reproducible checks. It must not require a database
service, model key, image provider, or social account.

## Decision

- Python 3.12, FastAPI, Pydantic v2, and Pydantic Settings for the backend.
- PostgreSQL is the future primary business database. No connection, service,
  or business schema is added in Phase 1.
- No ORM in Phase 1; evaluate SQLAlchemy 2.x + Alembic after the data model is
  frozen and database persistence enters scope.
- uv manages dependencies via `pyproject.toml` and committed `uv.lock`.
- pytest, Ruff (format and lint), and mypy provide local quality checks.
- GitHub Actions runs the locked checks on pull requests and pushes to `main`.
- No frontend project, Worker, Redis, Celery, LangGraph, Workflow Engine,
  Agent Orchestrator, real model provider, or image service in Phase 1.
- API major path is `/api/v1/`; JSON contracts use JSON Schema 2020-12 and a
  `schema_version` field. Timestamps are UTC ISO-8601 and IDs are UUIDv4 when
  those fields are introduced.
- Local unauthenticated health routes are for development/probes only and are
  not a public business API.

## Rationale and alternatives

Python keeps the later AI integration path in one backend language and is
available as Python 3.12 in the current development environment. FastAPI and
Pydantic provide request validation and OpenAPI with a small application
surface. TypeScript with Fastify/NestJS was considered but would add a second
ecosystem without a known team preference or present need. PostgreSQL is
approved for future relational project/run state, while deferring its service
avoids infrastructure in this health-only phase. The database-backed job
polling design remains a later proposal; no task system is selected here.

uv supplies dependency resolution and a committed cross-platform lock. pytest,
Ruff, and mypy are one focused Python quality stack. GitHub Actions is the
approved CI provider. Keeping the first phase backend-only avoids front-end
tooling and deployment cost before the product UI phase. Deferring ORM avoids
committing to persistence abstractions before schema freeze.

## Consequences

This creates a single Python package and a small dependency set. Local
development uses one application process; there is no database or worker to
operate. Later database deployment adds PostgreSQL backups, upgrades, access
control, and security review. Team familiarity with Python remains a delivery
risk to evaluate through Phase 1 review. The remote Actions workflow cannot be
confirmed until an authorized GitHub repository/remote exists.

## Revisit when

- The team cannot maintain Python or provides a stronger supported TypeScript
  standard.
- Production deployment, expected concurrency, or persistence requirements
  become known.
- The data model is frozen and an ORM/migration strategy is needed.
- A user-facing UI or durable workflow/worker is approved for a later phase.
