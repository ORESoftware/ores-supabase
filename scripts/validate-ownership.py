#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "ownership.json").read_text())
PROJECTS = ROOT / "projects"
errors: list[str] = []


def require(ok: bool, message: str) -> None:
    if not ok:
        errors.append(message)


require(POLICY.get("repository_role") == "fleet-provider-inventory-and-readback", "repository role drift")
require("product_provider_deployment" in POLICY.get("composition", {}), "product infra ownership missing")
require(POLICY.get("composition", {}).get("supabase_provider_inventory") == "ORESoftware/ores-supabase", "Supabase inventory owner drift")

projects = POLICY.get("projects", {})
actual_projects = sorted(p.name for p in PROJECTS.iterdir() if p.is_dir())
require(actual_projects == sorted(projects), f"project inventory drift: {actual_projects}")

for project_ref, project in projects.items():
    root = PROJECTS / project_ref
    allowed = set(project.get("allowed_files", []))
    require(project.get("overlay_state") == "compatibility-freeze", f"{project_ref}: overlay must remain frozen")
    require(project.get("product_infra_repository", "").endswith("-infra"), f"{project_ref}: product infra repository missing")
    actual = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file()
    }
    extra = sorted(actual - allowed)
    require(not extra, f"{project_ref}: product-owned files accumulated here: {extra}")
    for rel in actual:
        path = root / rel
        lower_name = rel.lower()
        for token in POLICY.get("secret_filename_tokens", []):
            require(token not in lower_name, f"{project_ref}: secret/private filename token `{token}` in {rel}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{project_ref}: binary file not allowed in provider overlay: {rel}")
            continue
        # Reject obvious credential-bearing material while allowing public project refs and schema names.
        secret_patterns = [
            r"(?i)(database_password|service_role_key|supabase_service_role_key|access_token|refresh_token)\s*[:=]",
            r"postgres(?:ql)?://[^\s:@]+:[^\s@]+@",
            r"(?i)BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY",
        ]
        for pattern in secret_patterns:
            require(re.search(pattern, text) is None, f"{project_ref}: credential-like content in {rel}")

if errors:
    for error in errors:
        print(f"provider-ownership: {error}", file=sys.stderr)
    raise SystemExit(1)
print(f"ores-supabase ownership policy: ok ({len(projects)} projects)")
