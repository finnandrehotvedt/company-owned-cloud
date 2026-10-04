# Decisions

## D1 — Small demonstrator, not enterprise cloud

- Date: 4 October 2026
- Source: direct user correction in receipt
  `desktop-owned-cloud-publication-20261004-001`
- Decision: build one bounded loopback lab with synthetic data and publish only
  measured demo evidence. Enterprise scaling is a separate document.

## D2 — Shared identity during measured app/data exit

One real Keycloak instance keeps the demo understandable and inside the host
budget. The measured exit moves the application and PostgreSQL data from
isolated target A to isolated target B. Identity export/issuer migration and
MFA re-enrolment remain explicit unmeasured limitations.

## D3 — No public demonstrator runtime in this release

The public websites present source, evidence, screenshots and honest limits.
The lab itself stays loopback-only and stopped after testing, avoiding a new
public attack surface or ongoing resource cost.

## D4 — Physical credentials are future options only

RFID, smart cards, fingerprint readers and similar physical-access hardware
are not purchased, integrated or tested in this release. They may be mentioned
as examples of later, separately assessed upgrades. No current security or
portability claim depends on them.

## D5 — Explicit host-loopback networking on CT109

CT109's exhausted default Docker address pool and existing bridge forwarding
state made a newly created demo bridge non-functional without changing shared
host firewall rules. The lab therefore uses host networking with every
listening process explicitly bound to `127.0.0.1` on reserved unique ports.
No wildcard or public listener is accepted. Target A and B still have separate
application ports, database ports and persistent volumes, and the measured
exit stops A before B is accepted.
