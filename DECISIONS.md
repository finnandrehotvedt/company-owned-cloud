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
