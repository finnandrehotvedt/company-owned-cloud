#!/usr/bin/env python3
"""Publish a small, sanitised aggregate of measured runtime receipts."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", "company-owned-cloud-lab")
SOURCE = ROOT / "runtime" / "evidence"
DESTINATION = ROOT / "evidence" / "measured-2026-10-04"
INPUTS = (
    "target-a.json",
    "persistence.json",
    "backup-timing.json",
    "exit-source.json",
    "exit-target.json",
    "exit-comparison.json",
    "exit-timing.json",
    "resource-peak.json",
)


def load(name: str) -> dict:
    return json.loads((SOURCE / name).read_text(encoding="utf-8"))


def main() -> None:
    missing = [name for name in INPUTS if not (SOURCE / name).is_file()]
    if missing:
        raise RuntimeError(f"missing evidence inputs: {missing}")
    running = subprocess.run(
        ["docker", "ps", "-q", "--filter", f"label=com.docker.compose.project={COMPOSE_PROJECT}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split()
    if running:
        raise RuntimeError("lab containers are still running")

    target_a = load("target-a.json")
    persistence = load("persistence.json")
    comparison = load("exit-comparison.json")
    backup = load("backup-timing.json")
    exit_timing = load("exit-timing.json")
    resources = load("resource-peak.json")
    tests = target_a["tests"]
    passed = (
        all(tests.values())
        and persistence["passed"]
        and comparison["passed"]
        and resources["peak_memory_bytes_aggregate"] < 2 * 1024**3
    )
    summary = {
        "schema_version": 1,
        "classification": "small_synthetic_demo",
        "passed": passed,
        "measured_on": "intentforce-ct109",
        "record_count": comparison["after"]["record_count"],
        "content_sha256": comparison["after"]["content_sha256"],
        "backup_elapsed_seconds": backup["elapsed_seconds"],
        "application_data_exit_elapsed_seconds": exit_timing["elapsed_seconds"],
        "sampled_peak_memory_bytes": resources["peak_memory_bytes_aggregate"],
        "authorization_checks": tests,
        "persistence_passed": persistence["passed"],
        "application_data_exit_passed": comparison["passed"],
        "identity_exit_measured": False,
        "enterprise_or_production_claim": False,
        "physical_access_hardware_tested": False,
        "final_runtime_state": "stopped",
    }
    if not passed:
        raise RuntimeError("aggregate evidence is not green")
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for name in INPUTS:
        shutil.copyfile(SOURCE / name, DESTINATION / name)
    (DESTINATION / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("Sanitised measured evidence published; final runtime state is stopped.")


if __name__ == "__main__":
    main()
