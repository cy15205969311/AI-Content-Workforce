# API and schema versioning

## API paths

Public API major versions use `/api/v{major}/`. Phase 1 implements `/api/v1/`
only. The liveness route `/health` remains unversioned for process probes; it
returns the same payload as `/api/v1/health`. OpenAPI JSON and Swagger UI are
under `/api/v1/openapi.json` and `/api/v1/docs`.

## JSON contracts

- JSON Schema draft: 2020-12.
- Every versioned response includes `schema_version`, currently `"1.0"`.
- Field names use `snake_case`; response schemas reject undocumented fields
  where practical.
- API errors use `{ "schema_version": "1.0", "error": { "code": ..., "message": ..., "request_id": ... } }`.
- Error messages are safe for clients; validation errors never echo submitted
  input values.
- Time values, when introduced, use UTC ISO-8601. IDs, when introduced, use
  UUIDv4. Cursor pagination is reserved for later business collection APIs.

The health and error JSON Schemas are in `docs/engineering/schemas/`. FastAPI
response models define the implemented health payload; tests verify the
observable response and versioned paths.

## Compatibility policy

Adding an optional response field may be compatible only if clients ignore
unknown fields. Removing/renaming a field or changing its meaning is breaking:
use a new API major version or an explicit migration plan. Breaking schema
changes increment the schema major version. Never silently change a published
field's meaning. Documentation, OpenAPI, JSON Schema, and tests must change
together.
