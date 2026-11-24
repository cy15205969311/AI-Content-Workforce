# Environment configuration

Settings use Pydantic Settings and read process environment variables plus an
optional `.env` file at the project root. Supported Phase 1 variables:

|Variable|Required|Allowed/default|Purpose|
|---|---|---|---|
|`APP_ENV`|No|`development` (default), `test`, `production`|Safe environment label returned by health|
|`LOG_LEVEL`|No|`INFO` (default), `DEBUG`, `WARNING`, `ERROR`|Application logger level|

Copy `.env.example` to `.env` for local overrides. Values shown in the example
are non-secret. `.env` and other `.env.*` files are ignored by Git; only
`.env.example` is allowlisted. Do not add API keys, passwords, or database
credentials in Phase 1 because no provider or database connector is configured.

Invalid environment values fail during application startup with field names but
without echoing submitted values. No setting contains a user directory or
machine-specific path. The database health state is `not_configured`; there is
no `DATABASE_URL` setting or connection attempt in this phase.
