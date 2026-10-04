#!/bin/sh
set -eu

cd /transfer
sha256sum -c source.dump.sha256
if ! restic snapshots --no-lock >/dev/null 2>&1; then
  restic init
fi
restic backup /transfer/source.dump /transfer/source.dump.sha256 --tag company-owned-cloud-exit
restic check
restic snapshots --json --latest 1
