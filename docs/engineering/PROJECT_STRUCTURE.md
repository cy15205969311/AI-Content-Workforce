# Project structure

Phase 1 uses one Python application package in `src/`; it is not a multi-package
monorepo. Product code, tests, engineering guidance, and research assets are kept
in separate areas.

```text
.
├── .github/workflows/ci.yml       # Pull request and main CI
├── docs/engineering/              # Actual engineering and API conventions
├── research/                      # Prior research, source snapshots, evidence
├── src/ai_content_workforce/      # FastAPI application package
│   ├── api/v1/                    # Versioned HTTP routes and response models
│   ├── core/                      # Settings and safe application logging
│   └── main.py                    # App factory and exception handling
├── tests/
│   ├── integration/               # In-process ASGI API tests
│   └── unit/                      # Settings and isolated behavior tests
├── .env.example                   # Safe local configuration example
├── .gitignore                     # Secrets, virtualenv, caches, generated data
├── .python-version                # Local Python minor version
├── CHANGELOG.md
├── pyproject.toml                 # Dependencies and quality tool configuration
└── uv.lock                        # Resolved dependency lock
```

No `skills/`, `workflows/`, ORM models, worker, frontend, or production storage
package is created yet. Add those only in their approved phases. `research/`
remains at the project root and is excluded from application linting.
