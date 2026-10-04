#!/usr/bin/env python3
"""Sample peak memory for only this Compose project's running containers."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from pathlib import Path


UNITS = {"B": 1, "KiB": 1024, "MiB": 1024**2, "GiB": 1024**3}


def bytes_from_human(value: str) -> int:
    match = re.fullmatch(r"([0-9.]+)(B|KiB|MiB|GiB)", value.strip())
    if not match:
        return 0
    return int(float(match.group(1)) * UNITS[match.group(2)])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--stop-file", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    peak: dict[str, int] = {}
    samples = 0
    while not args.stop_file.exists():
        listed = subprocess.run(
            ["docker", "ps", "-q", "--filter", f"label=com.docker.compose.project={args.project}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.split()
        if listed:
            result = subprocess.run(
                ["docker", "stats", "--no-stream", "--format", "{{.Name}}|{{.MemUsage}}", *listed],
                check=True,
                capture_output=True,
                text=True,
            )
            for line in result.stdout.splitlines():
                name, usage = line.split("|", 1)
                current = bytes_from_human(usage.split("/", 1)[0])
                peak[name] = max(current, peak.get(name, 0))
            samples += 1
        time.sleep(1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    receipt = {
        "schema_version": 1,
        "sampling_interval_seconds": 1,
        "sample_count": samples,
        "peak_memory_bytes_by_container": dict(sorted(peak.items())),
        "peak_memory_bytes_aggregate": sum(peak.values()),
    }
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
