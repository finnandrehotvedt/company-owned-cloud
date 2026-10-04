# Company-Owned Cloud Lab

Own the source. Own the backup. Prove the exit.

This open-source, small-footprint lab demonstrates a company-controlled notes
service with PostgreSQL, real Keycloak OIDC, role checks, a TOTP-enrolment
state, content-minimised audit logging and encrypted Restic backups. Its main
test exports synthetic data from target A, stops A, restores into target B and
accepts B only when record count and a deterministic content hash match.

It is a bounded teaching and evidence project—not an enterprise cloud product,
managed service, compliance certificate or production migration kit.

## Measured result

The CT109 rehearsal on 4 October 2026 passed:

- 2 synthetic records restored with matching SHA-256 content state;
- missing token, wrong audience, insufficient role and MFA-pending identity
  rejected; valid user/admin paths accepted;
- encrypted backup checked and restored;
- target A stopped before target B acceptance;
- application/data exit: 24.843 seconds; backup: 6.457 seconds;
- sampled aggregate peak memory: 697,502,266 bytes (about 665 MiB);
- final runtime state: stopped.

See [`evidence/measured-2026-10-04/summary.json`](evidence/measured-2026-10-04/summary.json).
These numbers describe one small synthetic run on one host, not a capacity or
availability benchmark. Identity remained shared and was not migrated.

## Run it

Requirements: Linux, Docker Engine, `docker-compose` 1.29+, Python 3.11+ with
PyYAML/jsonschema, `curl`, five free loopback ports and at least 4 GiB free
disk.

```sh
git clone https://github.com/finnandrehotvedt/company-owned-cloud.git
cd company-owned-cloud
scripts/labctl integration
```

The command generates local credentials under ignored `runtime/secrets/`, runs
the complete rehearsal and stops all lab containers. It never needs customer
data or a cloud account. Ordinary `scripts/labctl stop` retains volumes;
`scripts/labctl reset` is the explicit destructive lab reset.

## What to read

- [`SPECIFICATION.md`](SPECIFICATION.md) — locked scope and acceptance contract
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — components and measured boundary
- [`docs/RUNBOOK.md`](docs/RUNBOOK.md) — lifecycle and recovery commands
- [`docs/IDENTITY-MFA.md`](docs/IDENTITY-MFA.md) — identity and honest MFA proof
- [`docs/THREAT-MODEL.md`](docs/THREAT-MODEL.md) — controls and exclusions
- [`docs/SCALING.md`](docs/SCALING.md) — unmeasured production roadmap
- [`docs/KNOWN-LIMITATIONS.md`](docs/KNOWN-LIMITATIONS.md) — what this does not prove
- [`docs/OPERATOR-TRAINING.md`](docs/OPERATOR-TRAINING.md) — a short learning exercise

RFID cards, fingerprint smart cards/readers and similar physical technology
are only examples of possible later upgrades. No card is ordered, included,
recommended or tested here.

## Public mirrors

The canonical public mirrors are intended to carry the identical `main`
commit:

- GitHub: <https://github.com/finnandrehotvedt/company-owned-cloud>
- GitLab: <https://gitlab.com/finnandrehotvedt/company-owned-cloud>

Source written for this project is Apache-2.0. Third-party components retain
their own licences; see [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).
