#!/usr/bin/env python3
"""Run positive and negative HTTP acceptance checks without exposing tokens."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IDENTITY = "http://127.0.0.1:18790/realms/company-owned-cloud/protocol/openid-connect/token"
SYNTHETIC_NOTES = (
    {"title": "Portable policy", "body": "Synthetic record: exports must be testable and reversible."},
    {"title": "Recovery rehearsal", "body": "Synthetic record: restore evidence belongs with the source."},
)


def secret(name: str) -> str:
    return (ROOT / "runtime" / "secrets" / name).read_text(encoding="utf-8").strip()


def token(username: str, password_name: str, client_id: str = "portable-notes") -> tuple[int, str | None]:
    body = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "grant_type": "password",
            "username": username,
            "password": secret(password_name),
        }
    ).encode("ascii")
    request = urllib.request.Request(
        IDENTITY,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            return response.status, json.load(response)["access_token"]
    except urllib.error.HTTPError as error:
        error.read()
        return error.code, None


def api(base: str, method: str, path: str, access_token: str | None = None, payload: object | None = None) -> tuple[int, object | None]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    request = urllib.request.Request(base + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            raw = response.read()
            return response.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as error:
        raw = error.read()
        try:
            parsed = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            parsed = None
        return error.code, parsed


def check(condition: bool, name: str, results: dict[str, bool]) -> None:
    results[name] = bool(condition)
    if not condition:
        raise RuntimeError(f"acceptance check failed: {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--seed", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    started = time.monotonic()
    results: dict[str, bool] = {}
    status, health = api(args.base, "GET", "/healthz")
    check(status == 200 and health["target"] == args.target, "health", results)

    status, _ = api(args.base, "GET", "/api/whoami")
    check(status == 401, "missing_token_rejected", results)

    status, user_token = token("automation-user", "automation_password")
    check(status == 200 and bool(user_token), "user_token_issued", results)
    status, identity = api(args.base, "GET", "/api/whoami", user_token)
    check(status == 200 and identity["username"] == "automation-user", "valid_user_accepted", results)
    status, _ = api(args.base, "GET", "/api/admin/audit-summary", user_token)
    check(status == 403, "insufficient_role_rejected", results)

    status, wrong_token = token("automation-user", "automation_password", "wrong-audience")
    check(status == 200 and bool(wrong_token), "wrong_audience_token_issued", results)
    status, _ = api(args.base, "GET", "/api/whoami", wrong_token)
    check(status == 401, "wrong_audience_rejected", results)

    status, _ = token("mfa-pending", "mfa_pending_password")
    check(status in {400, 401}, "mfa_enrolment_required", results)

    status, admin_token = token("cloud-admin", "cloud_admin_password")
    check(status == 200 and bool(admin_token), "admin_token_issued", results)
    status, _ = api(args.base, "GET", "/api/admin/audit-summary", admin_token)
    check(status == 200, "admin_role_accepted", results)

    status, listed = api(args.base, "GET", "/api/notes", user_token)
    check(status == 200, "notes_read", results)
    if args.seed:
        existing = {note["title"] for note in listed["notes"]}
        for note in SYNTHETIC_NOTES:
            if note["title"] not in existing:
                status, _ = api(args.base, "POST", "/api/notes", user_token, note)
                check(status == 201, f"seed_{note['title'].lower().replace(' ', '_')}", results)

    status, state = api(args.base, "GET", "/api/state", user_token)
    check(status == 200 and state["record_count"] >= (2 if args.seed else 0), "state_available", results)
    status, audit = api(args.base, "GET", "/api/admin/audit-safety", admin_token)
    check(status == 200 and audit["safe"] is True, "audit_content_minimised", results)

    receipt = {
        "schema_version": 1,
        "target": args.target,
        "base_url": args.base,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "tests": results,
        "state": {
            "record_count": state["record_count"],
            "content_sha256": state["content_sha256"],
        },
        "audit": {"safe": audit["safe"], "event_count": audit["event_count"]},
        "secrets_or_tokens_emitted": False,
    }
    output = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
