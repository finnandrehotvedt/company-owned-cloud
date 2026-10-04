#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


operation, started, ended, destination = sys.argv[1:5]
payload = {
    "schema_version": 1,
    "operation": operation,
    "elapsed_seconds": round((int(ended) - int(started)) / 1000, 3),
    "measurement": "wall-clock on the small CT109 demonstrator",
}
Path(destination).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
