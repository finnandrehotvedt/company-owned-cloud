#!/bin/sh
set -eu

if [ -z "${DATABASE_PASSWORD_FILE:-}" ] || [ ! -r "$DATABASE_PASSWORD_FILE" ]; then
  echo "database password file unavailable" >&2
  exit 78
fi
export PGPASSWORD="$(cat "$DATABASE_PASSWORD_FILE")"
umask 077
pg_dump --format=custom --no-owner --no-acl --file=/transfer/source.dump
cd /transfer
sha256sum source.dump > source.dump.sha256
pg_restore --list source.dump >/dev/null
echo "Source export and local archive validation passed."
