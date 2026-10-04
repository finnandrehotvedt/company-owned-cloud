#!/usr/bin/env python3
"""Create local demo secrets without printing their values."""

from __future__ import annotations

import json
import os
import secrets
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
SECRETS = RUNTIME / "secrets"
NAMES = (
    "db_a_password",
    "db_b_password",
    "keycloak_admin_password",
    "restic_password",
    "automation_password",
    "cloud_admin_password",
    "mfa_pending_password",
)
SERVICE_OWNERS = {
    "db_a_password": 10001,
    "db_b_password": 10001,
    "keycloak_admin_password": 1000,
}


def create_secret(path: Path) -> bool:
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        if path.stat().st_mode & 0o077:
            path.chmod(0o600)
        return False
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(secrets.token_urlsafe(36))
        handle.write("\n")
    return True


def main() -> None:
    RUNTIME.mkdir(mode=0o700, exist_ok=True)
    SECRETS.mkdir(mode=0o700, exist_ok=True)
    (RUNTIME / "evidence").mkdir(mode=0o700, exist_ok=True)
    created = [name for name in NAMES if create_secret(SECRETS / name)]
    for name, uid in SERVICE_OWNERS.items():
        path = SECRETS / name
        os.chown(path, uid, 0)
        path.chmod(0o600)
    receipt = {
        "schema_version": 1,
        "secret_values_printed": False,
        "secret_files": list(NAMES),
        "created_count": len(created),
        "existing_count": len(NAMES) - len(created),
    }
    (RUNTIME / "initialisation.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"Runtime ready: {len(created)} secret file(s) created; values were not printed.")


if __name__ == "__main__":
    main()
