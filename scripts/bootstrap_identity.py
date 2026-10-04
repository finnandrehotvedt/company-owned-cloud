#!/usr/bin/env python3
"""Idempotently create synthetic Keycloak lab users and role mappings."""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:18790"
REALM = "company-owned-cloud"


def secret(name: str) -> str:
    return (ROOT / "runtime" / "secrets" / name).read_text(encoding="utf-8").strip()


def call(method: str, path: str, token: str | None = None, payload: object | None = None) -> tuple[int, object | None]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            raw = response.read()
            return response.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as error:
        raw = error.read()
        return error.code, json.loads(raw) if raw else None


def admin_token() -> str:
    form = urllib.parse.urlencode(
        {
            "client_id": "admin-cli",
            "grant_type": "password",
            "username": "lab-admin",
            "password": secret("keycloak_admin_password"),
        }
    ).encode("ascii")
    request = urllib.request.Request(
        BASE + "/realms/master/protocol/openid-connect/token",
        data=form,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        return json.load(response)["access_token"]


def ensure_user(token: str, username: str, password_name: str, roles: list[str], required_actions: list[str]) -> None:
    query = urllib.parse.urlencode({"username": username, "exact": "true"})
    status, found = call("GET", f"/admin/realms/{REALM}/users?{query}", token)
    if status != 200:
        raise RuntimeError(f"user lookup failed for {username}: HTTP {status}")
    user_payload = {
        "username": username,
        "firstName": "Synthetic",
        "lastName": username,
        "email": f"{username}@example.invalid",
        "enabled": True,
        "emailVerified": True,
        "requiredActions": required_actions,
        "attributes": {"demoClassification": ["synthetic-only"]},
    }
    if found:
        user_id = found[0]["id"]
        status, _ = call("PUT", f"/admin/realms/{REALM}/users/{user_id}", token, user_payload)
        if status != 204:
            raise RuntimeError(f"user update failed for {username}: HTTP {status}")
    else:
        status, _ = call("POST", f"/admin/realms/{REALM}/users", token, user_payload)
        if status != 201:
            raise RuntimeError(f"user create failed for {username}: HTTP {status}")
        status, found = call("GET", f"/admin/realms/{REALM}/users?{query}", token)
        if status != 200 or not found:
            raise RuntimeError(f"created user not found: {username}")
        user_id = found[0]["id"]

    status, _ = call(
        "PUT",
        f"/admin/realms/{REALM}/users/{user_id}/reset-password",
        token,
        {"type": "password", "temporary": False, "value": secret(password_name)},
    )
    if status != 204:
        raise RuntimeError(f"password reset failed for {username}: HTTP {status}")

    status, available_roles = call("GET", f"/admin/realms/{REALM}/roles", token)
    if status != 200:
        raise RuntimeError(f"role lookup failed: HTTP {status}")
    mappings = [role for role in available_roles if role.get("name") in roles]
    if {role["name"] for role in mappings} != set(roles):
        raise RuntimeError(f"required realm role missing for {username}")
    status, _ = call(
        "POST",
        f"/admin/realms/{REALM}/users/{user_id}/role-mappings/realm",
        token,
        mappings,
    )
    if status != 204:
        raise RuntimeError(f"role mapping failed for {username}: HTTP {status}")


def main() -> None:
    last_error: Exception | None = None
    for _ in range(40):
        try:
            token = admin_token()
            break
        except Exception as error:
            last_error = error
            time.sleep(2)
    else:
        raise RuntimeError(f"identity not ready: {type(last_error).__name__}")

    ensure_user(token, "automation-user", "automation_password", ["cloud-user"], [])
    ensure_user(token, "cloud-admin", "cloud_admin_password", ["cloud-user", "cloud-admin"], [])
    ensure_user(token, "mfa-pending", "mfa_pending_password", ["cloud-user"], ["CONFIGURE_TOTP"])
    print("Synthetic identity users and roles are ready; no credential values were printed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"identity bootstrap failed: {error}", file=sys.stderr)
        raise SystemExit(1)
