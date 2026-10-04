# Small business-owned cloud demonstrator

Version: `0.1-draft`  
Date: 4 October 2026  
Owner: IntentForce / Finn André Hotvedt

## Outcome

Build one isolated, reproducible self-host lab containing a synthetic notes
application, PostgreSQL data, a real local identity provider, bounded audit
logging and encrypted backups. Demonstrate and measure export from target A,
shutdown of target A, restore into isolated target B and successful authorised
use on B.

The result teaches ownership and exit skills. It does not replace a company's
current services and makes no production availability, compliance, capacity or
security-certification claim.

## Locked small-demo scope

- one tiny demonstrator application and synthetic records;
- one Keycloak identity service for the local lab, with real OIDC and written
  TOTP/WebAuthn enrolment instructions;
- two isolated application/database targets used only for the measured exit;
- structured, content-minimised audit logging;
- encrypted Restic backup, integrity check and restore;
- source/config validation, positive and negative authorisation tests;
- no public runtime, no customer migration, no paid infrastructure, no HA,
  no Kubernetes/OpenStack and no production service changes.

Identity remains a shared lab dependency during the measured application/data
exit. Exporting identity, rotating issuers and re-enrolling MFA are documented
but are not called measured in this release.

## Observed CT109 capacity and lab budget

Observed before build on 4 October 2026:

- 10 logical CPUs;
- 12 GiB RAM total, 9 GiB available;
- 7.3 GiB free on the Docker/root filesystem, which was already 97% used;
- existing production and lab containers remain untouched.

The Compose contract must enforce a concurrent maximum below 2 logical CPUs
and 2 GiB RAM. New images, build cache, source, volumes, backup and evidence
must stay below 2.5 GiB combined. Build/release stops and removes only its own
disposable cache/images if host free space would fall below 4 GiB. Persistent
synthetic volumes remain tiny and are retained after normal stop.

Reserved loopback ports:

- `127.0.0.1:18780` — target A application;
- `127.0.0.1:18781` — target B application;
- `127.0.0.1:18790` — Keycloak lab identity.

No automatic restart policy is allowed. The final resting state is stopped.

## Acceptance

1. A fresh clone can initialise non-secret runtime configuration and generated
   secret files without printing their values.
2. Compose validation and the reusable-environment audit pass.
3. Keycloak, target A and its database become healthy within the resource
   budget; only loopback listeners appear.
4. OIDC login succeeds for the synthetic automation user; missing token, wrong
   audience, insufficient role and MFA-pending user cases fail closed.
5. Synthetic notes can be created/read and audit records contain no note body,
   password or bearer token.
6. A PostgreSQL export is checksummed, backed up into an encrypted Restic
   repository and passes `restic check`.
7. Target A is stopped before target B is accepted. Target B restores the same
   record count and deterministic content hashes, passes authorised use and has
   no network dependency on target A.
8. Actual backup, restore and exit elapsed times, image/disk use and peak
   container memory are captured as demo measurements only.
9. Stop/start proves retained state; final stop leaves no running lab
   containers or loopback listeners.
10. Public mirrors advertise one identical exact commit and a credential-free
    clone rebuilds/tests the lab.

## Scaling boundary

`docs/SCALING.md` may describe how a real engagement adds external TLS,
separate identity, protected backup domains, observability, HA, capacity tests,
operator coverage and compliance work. Those are a roadmap, not evidence of
this demo.
