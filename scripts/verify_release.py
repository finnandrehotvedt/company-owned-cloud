#!/usr/bin/env python3
"""Credential-free source/evidence checks suitable for a fresh clone."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:password|api[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^$<{][^'\"]{7,}"),
)


def main() -> None:
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.splitlines()
    if any(path == "runtime" or path.startswith("runtime/") for path in tracked):
        raise RuntimeError("runtime state is tracked")
    findings: list[str] = []
    for relative in tracked:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(pattern.search(text) for pattern in FORBIDDEN):
            findings.append(relative)
    if findings:
        raise RuntimeError(f"possible credential material in: {sorted(set(findings))}")
    summary = json.loads(
        (ROOT / "evidence/measured-2026-10-04/summary.json").read_text(encoding="utf-8")
    )
    if not summary["passed"] or summary["final_runtime_state"] != "stopped":
        raise RuntimeError("published evidence is not green/stopped")
    if summary["physical_access_hardware_tested"] is not False:
        raise RuntimeError("physical hardware claim escaped the scope boundary")
    print("Tracked-source secret scan and published evidence contract passed.")


if __name__ == "__main__":
    main()
