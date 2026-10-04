#!/bin/sh
set -eu

find /restore -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
restic check
restic restore latest --target /restore --tag company-owned-cloud-exit
cd /restore/transfer
sha256sum -c source.dump.sha256
echo "Encrypted backup restored and checksum validated."
