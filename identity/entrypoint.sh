#!/bin/sh
set -eu

secret_file=${KEYCLOAK_ADMIN_PASSWORD_FILE:-}
if [ -z "$secret_file" ] || [ ! -r "$secret_file" ]; then
  echo "KEYCLOAK_ADMIN_PASSWORD_FILE is missing or unreadable" >&2
  exit 78
fi

KC_BOOTSTRAP_ADMIN_PASSWORD=$(cat "$secret_file")
export KC_BOOTSTRAP_ADMIN_PASSWORD
unset KEYCLOAK_ADMIN_PASSWORD_FILE
mkdir -p /opt/keycloak/data/import
cp /opt/lab/realm.json /opt/keycloak/data/import/realm.json
exec /opt/keycloak/bin/kc.sh "$@"
