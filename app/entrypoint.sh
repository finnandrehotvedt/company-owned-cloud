#!/bin/sh
set -eu

if [ -z "${DATABASE_PASSWORD_FILE:-}" ] || [ ! -r "$DATABASE_PASSWORD_FILE" ]; then
  echo "DATABASE_PASSWORD_FILE is missing or unreadable" >&2
  exit 78
fi

DATABASE_PASSWORD=$(cat "$DATABASE_PASSWORD_FILE")
export DATABASE_PASSWORD
unset DATABASE_PASSWORD_FILE
exec "$@"
