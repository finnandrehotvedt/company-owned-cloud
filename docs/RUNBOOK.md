# Operator runbook

## Requirements

- Linux with Docker Engine and `docker-compose` 1.29 or newer;
- Python 3.11 or newer with PyYAML and jsonschema for local validation;
- `curl`, at least 4 GiB free disk and the five reserved loopback ports;
- no customer, production or personal data.

## Complete measured rehearsal

```sh
scripts/labctl integration
```

This validates source/configuration, creates local secret files, starts target
A, runs positive and negative authorisation tests, proves persistence, creates
and checks an encrypted Restic backup, stops A, restores to B, compares count
and content hash, records resource samples and stops the entire lab.

For an isolated second rehearsal on the same Docker host, set a distinct
project name, for example
`COMPOSE_PROJECT_NAME=company-owned-cloud-fresh scripts/labctl integration`.
The fixed loopback ports must still be free.

## Smaller lifecycle commands

```sh
scripts/labctl init
scripts/labctl validate
scripts/labctl start-a
scripts/labctl test-a
scripts/labctl persistence
scripts/labctl backup
scripts/labctl exit-test
scripts/labctl status
scripts/labctl stop
```

`stop` removes this project's containers but retains named volumes and
generated secret files. `reset` is the explicit destructive command: it
removes only this Compose project's named volumes, while retaining generated
secret files. Use it only when a clean synthetic rehearsal is intended.

Evidence is written to `evidence/measured-2026-10-04/`. Secret values, bearer
tokens and note bodies are not emitted there.

## Health and recovery

- Identity: `http://127.0.0.1:18790/realms/company-owned-cloud`
- Target A readiness: `http://127.0.0.1:18780/readyz`
- Target B readiness: `http://127.0.0.1:18781/readyz`

If a command fails, inspect only this project with
`COMPOSE_PROJECT_NAME=company-owned-cloud-lab docker-compose -f compose.yaml ps`
and bounded `logs --tail=100 SERVICE`. Run `scripts/labctl stop`; do not delete
volumes until the failure evidence has been understood.
