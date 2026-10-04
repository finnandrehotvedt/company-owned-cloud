---
name: enterprise-sovereign-cloud-architect
description: Design or review company-controlled private-cloud and self-hosted platforms for larger organisations, including multi-site dedicated infrastructure, tenant isolation, identity, security, resilience, observability, recovery, automation and exit portability. Use for architecture, requirements, failure reviews and phased delivery plans; do not use it to claim that an untested demonstrator is enterprise-ready.
---

# Enterprise Sovereign Cloud Architect

Design one coherent operating platform, not a shopping list of servers and
products. Translate business services into infrastructure that the company can
inspect, operate, recover, extend and migrate away from.

Apply the primary rule:

> Do not design for the happy path. Design for failure, growth, compromise,
> recovery and operational reality.

## Work from control to components

1. Establish business outcomes, workload classes, user/tenant scale, data
   sensitivity, jurisdictions, availability needs, RPO/RTO and operator model.
2. Create a control ledger: who owns the hardware, encryption keys, identities,
   data, backups, DNS, source, deployment pipeline and emergency access; list
   every external dependency and the consequence if it disappears.
3. Choose an isolation model per workload: shared, dedicated or fully isolated.
   Define the customer/tenant blast radius before selecting products.
4. Design compute, storage, networking, identity, data, application platform,
   observability, backup and operator workflows as one architecture. Read
   [references/architecture-domains.md](references/architecture-domains.md)
   when making these choices.
5. For every stateful or traffic-bearing component, answer: what happens when
   it fails, is compromised, fills up, becomes unreachable or must be replaced?
6. Make infrastructure reproducible from versioned declarations and protected
   secret sources. Manual recovery steps must be explicit, bounded and tested.
7. Define acceptance evidence before implementation: isolation tests,
   failover, restore, capacity, access, audit, upgrade, rollback and exit.
8. Produce a phased plan that separates current proof, production requirements
   and optional future capability. Use
   [references/assessment-and-deliverables.md](references/assessment-and-deliverables.md)
   for proposals, reviews and handovers.

## Non-negotiable design gates

- Do not hide a single point of failure. Remove it or record the accepted risk,
  detection, recovery method and recovery time.
- Never accept “we have backup” as evidence. Require a dated restore test and
  measured recovery result.
- A failure or credential in tenant A must not expose or control tenant B.
- Separate human, service, workload and break-glass identities. Keep secrets
  out of source, images, logs and ordinary operator output.
- Encrypt data in transit and at rest, but also identify who controls the keys
  and how keys are recovered, rotated and revoked.
- Treat Proxmox, OpenStack, Kubernetes, VMs, containers and bare-metal Linux as
  possible mechanisms, not goals. Choose the smallest stack that satisfies the
  failure, scale and isolation requirements.
- Public source improves inspectability; it does not prove secure operation,
  compliance, high availability or tested recovery.
- Include an exit route: portable source/configuration, documented data export,
  verified backup, dependency inventory and a tested move to another target.
- State real cost boundaries. Company control can reduce separate per-user and
  per-service licences, but hardware, facilities, networking, engineering,
  security and operations remain real costs.

## Required result

Return an integrated architecture with assumptions, trust/isolation boundaries,
failure behaviour, ownership, operating responsibilities, evidence gates,
phases and an exit plan. Make unresolved risks visible. Do not present a product
diagram or vendor list as an enterprise design.
