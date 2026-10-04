# Company-Owned Cloud agent contract

This repository owns one small, isolated, synthetic-data demonstration of a
business-owned application/data stack and a measured exit between two local
targets. It is not an enterprise platform or a production migration.

## Ownership

- Canonical project root: `/srv/codex-workspaces/projects/company-owned-cloud`
- Runtime owner: `intentforce-ct109` resident operator
- Compose project: `company-owned-cloud-lab`
- One writer owns source and runtime changes at a time.

## Hard boundaries

- Never use customer data, production logs, production credentials or private
  topology.
- Never attach the lab to an existing production network, database, identity
  system, proxy or public listener.
- Bind all browser-facing lab ports to loopback.
- Store generated secrets only below ignored `runtime/secrets/` with mode 0600.
- No HA cluster, Kubernetes, OpenStack, production SLA or enterprise-ready
  claim belongs in this release.
- The measured exit covers this demo application and its synthetic database.
  Identity portability, multi-site disaster recovery and production scale are
  documented future work unless separately tested.
- The normal resting state is stopped. Ordinary stop never deletes volumes.

## Required release evidence

- pinned images/dependencies and third-party notices;
- configuration/schema validation and secret scan;
- positive integration, negative authorization, encrypted backup/restore and
  measured target-A-to-target-B exit tests;
- stop/start persistence with loopback-only port verification;
- exact source commit, release checksum and anonymous fresh-clone Docker test;
- sanitised machine-readable evidence and explicit known limitations;
- public-site publication only after source mirrors and runtime evidence are
  green.

Use `apply_patch` for source edits. Keep generated runtime state and credentials
out of Git. Update `.cognitive-memory/working-memory.md` at each durable
milestone.
