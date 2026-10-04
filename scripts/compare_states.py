#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


before_path, after_path, output_path = map(Path, sys.argv[1:4])
before = json.loads(before_path.read_text(encoding="utf-8"))["state"]
after = json.loads(after_path.read_text(encoding="utf-8"))["state"]
receipt = {
    "schema_version": 1,
    "before": before,
    "after": after,
    "record_count_equal": before["record_count"] == after["record_count"],
    "content_sha256_equal": before["content_sha256"] == after["content_sha256"],
}
receipt["passed"] = receipt["record_count_equal"] and receipt["content_sha256_equal"]
output_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
if not receipt["passed"]:
    raise SystemExit("state comparison failed")
print("Record count and deterministic content hash match.")
