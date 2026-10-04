# Threat model

## Protected assets

- generated local credentials;
- synthetic notes and database backups;
- audit integrity;
- source/configuration provenance;
- the guarantee that no service is publicly exposed.

## Controls demonstrated

- loopback-only listeners on fixed ports;
- OIDC issuer, signature and audience verification;
- role-based user/admin separation and fail-closed negative tests;
- a TOTP enrolment-required identity state;
- non-root application process, dropped capabilities and read-only root FS;
- generated `0600` secrets excluded from Git;
- content-minimised structured audit events;
- encrypted Restic repository plus archive/checksum validation;
- stopped source before target acceptance and deterministic state comparison;
- pinned container image digests and hash-locked Python dependencies.

## Explicitly out of scope

This is not internet hardened, highly available, capacity tested, certified or
monitored as a production service. Keycloak runs in development mode with its
embedded lab store. Host compromise, malicious Docker administrators, supply
chain compromise outside the pinned artefacts, secure off-site custody and
physical access are not solved here.

RFID cards, fingerprint smart cards/readers and other physical credentials are
possible future integration topics only. No device has been purchased,
integrated or security-tested, and no present claim depends on one.
