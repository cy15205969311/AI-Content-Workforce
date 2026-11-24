"""Static checks for the published JSON Schema examples and secret ignore rules."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_published_schemas_use_json_schema_2020_12() -> None:
    schema_dir = PROJECT_ROOT / "docs" / "engineering" / "schemas"

    for schema_file in schema_dir.glob("*.schema.json"):
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["properties"]["schema_version"] == {"const": "1.0"}


def test_dotenv_is_ignored_but_example_is_allowlisted() -> None:
    ignore_rules = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

    assert ".env" in ignore_rules
    assert ".env.*" in ignore_rules
    assert "!.env.example" in ignore_rules


def test_dependency_lock_uses_public_registry_only() -> None:
    lock_text = (PROJECT_ROOT / "uv.lock").read_text(encoding="utf-8")

    assert "https://pypi.org/simple/" in lock_text
    assert "pypi.tuna" not in lock_text
