#!/bin/sh
set -eu

if [ -z "${DATABASE_PASSWORD_FILE:-}" ] || [ ! -r "$DATABASE_PASSWORD_FILE" ]; then
  echo "database password file unavailable" >&2
  exit 78
fi
export PGPASSWORD="$(cat "$DATABASE_PASSWORD_FILE")"
cd /restore/transfer
sha256sum -c source.dump.sha256
pg_restore --clean --if-exists --no-owner --no-acl --dbname="$PGDATABASE" source.dump
echo "Target B database import completed."
