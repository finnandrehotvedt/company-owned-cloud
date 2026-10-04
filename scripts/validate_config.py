#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    platform = json.loads((ROOT / "config/platform.json").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "config/platform.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(platform, schema)
    compose = yaml.safe_load((ROOT / "compose.yaml").read_text(encoding="utf-8"))
    published = []
    for service_name, service in compose["services"].items():
        for item in service.get("ports", []):
            published.append((service_name, str(item)))
    if published:
        raise RuntimeError(f"unexpected published ports: {published}")
    host_services = {"identity", "db-a", "app-a", "db-b", "app-b", "exporter", "importer"}
    for service_name in host_services:
        if compose["services"][service_name].get("network_mode") != "host":
            raise RuntimeError(f"expected explicit host networking: {service_name}")
    serialised = json.dumps(compose["services"], sort_keys=True)
    for required in ("127.0.0.1", "18780", "18781", "18782", "18783", "18790"):
        if required not in serialised:
            raise RuntimeError(f"missing loopback/port contract: {required}")
    for service_name, service in compose["services"].items():
        if service.get("restart") not in {None, "no"}:
            raise RuntimeError(f"restart policy is not bounded: {service_name}")
    if platform["limits"]["aggregate_cpus"] > 2 or platform["limits"]["aggregate_memory_mib"] > 2048:
        raise RuntimeError("platform resource ceiling exceeds contract")
    print("Configuration schema, loopback listeners and bounded lifecycle validated.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"configuration validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
