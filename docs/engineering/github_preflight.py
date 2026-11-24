"""Produce a redacted publication inventory; never print matching secret values."""

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    "api_key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b"),
    "aws_access_id": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    "credential_url": re.compile(r"(?:https?|postgres(?:ql)?|mysql)://[^\s/:]+:[^\s/@]+@"),
}


def scan() -> None:
    cached = set(
        filter(
            None,
            subprocess.check_output(["git", "ls-files", "--cached", "-z"], cwd=ROOT)
            .decode()
            .split("\0"),
        )
    )
    candidates = (
        subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
        )
        .decode()
        .split("\0")
    )
    inventory = []
    findings = []
    for name in sorted(set(filter(None, candidates))):
        if name == "docs/engineering/GITHUB_PUBLICATION_SCAN.json":
            continue
        path = ROOT / name
        if not path.is_file():
            findings.append({"path": name, "kind": "non_regular_file"})
            continue
        data = (
            subprocess.check_output(["git", "show", f":{name}"], cwd=ROOT)
            if name in cached
            else path.read_bytes()
        )
        inventory.append(
            {"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        )
        content = data.decode("utf-8", errors="replace")
        for kind, pattern in PATTERNS.items():
            if pattern.search(content):
                findings.append({"path": name, "kind": kind})
        for variable, value in os.environ.items():
            if (
                re.search(r"(?:SECRET|PASSWORD|TOKEN|API_KEY|ACCESS_KEY|OAI_KEY)", variable)
                and len(value) >= 12
                and value in content
            ):
                findings.append({"path": name, "kind": "matches_sensitive_environment_value"})
        for variable, value in os.environ.items():
            if (
                re.search(r"(?:SECRET|PASSWORD|TOKEN|API_KEY|ACCESS_KEY|OAI_KEY)", variable)
                and len(value) >= 12
                and value in content
            ):
                findings.append({"path": name, "kind": "matches_sensitive_environment_value"})
        if path.suffix.lower() in {".pem", ".key", ".pfx", ".p12", ".sqlite", ".db"}:
            findings.append({"path": name, "kind": "sensitive_file_extension"})

    research_files = []
    for path in (ROOT / "research").rglob("*"):
        if path.is_file() and ".git" not in path.relative_to(ROOT / "research").parts:
            research_files.append(path.relative_to(ROOT).as_posix())

    result = {
        "scope": "proposed public files; all research excluded from initial staging",
        "limitations": "Pattern scan is not proof of absence of secrets or private material.",
        "candidate_files": inventory,
        "findings": findings,
        "research_excluded_file_count": len(research_files),
        "research_publication": "deferred; raw clones, evidence, metadata and baselines stay local",
    }
    out = ROOT / "docs/engineering/GITHUB_PUBLICATION_SCAN.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "candidates": len(inventory),
                "findings": findings,
                "research_excluded": len(research_files),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    scan()
