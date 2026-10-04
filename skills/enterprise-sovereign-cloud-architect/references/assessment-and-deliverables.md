# Assessment and deliverables

## Minimum discovery

Capture:

- business services, owners, users, tenants and growth;
- workload inventory and state dependencies;
- data classes, locations, retention and jurisdiction;
- availability, RPO/RTO and maintenance constraints;
- current identity, DNS, networking, backup and monitoring dependencies;
- operator staffing, on-call capability and support boundaries;
- current contracts, per-user/per-service costs and required exit dates;
- migration constraints and acceptable coexistence periods.

Unknowns must become assumptions or explicit discovery work, never invisible
architecture facts.

## Integrated architecture output

Provide:

1. business-service and workload map;
2. control and external-dependency ledger;
3. shared/dedicated/isolated placement decision;
4. trust, tenant and administrative boundaries;
5. compute, storage, network, identity, data and application design;
6. failure matrix for component, provider and site loss;
7. observability and operator model;
8. backup, restore, RPO/RTO and disaster-recovery design;
9. infrastructure-as-code, release, upgrade and rollback workflow;
10. capacity assumptions and validation plan;
11. security and compliance evidence plan;
12. migration, coexistence, handover and tested exit plan.

## Delivery phases

Use evidence-gated phases rather than declaring enterprise readiness early:

- **Discovery:** verified requirements and dependency inventory.
- **Isolated proof:** synthetic data, no production dependency, bounded limits.
- **Production foundation:** identity, networking, secrets, observability,
  backup and operating ownership established.
- **Workload pilot:** one reversible, non-critical workload with measured
  recovery and exit.
- **Resilience:** component/site failure and capacity tests pass.
- **Controlled expansion:** additional workloads or tenants enter only after
  their isolation, recovery and operator acceptance checks pass.
- **Handover or managed operation:** responsibilities, access, source,
  documentation, training, escalation and exit are signed off.

## Evidence questions

- When was restore last tested, into what target, and what were measured RPO
  and RTO?
- Which component still causes a complete outage or cross-tenant risk?
- Which person or service can decrypt production data?
- Can the platform start and authenticate if each external dependency is down?
- Can infrastructure be rebuilt from versioned source and protected secrets?
- Can one tenant be deleted or exported without affecting another?
- Can the company move a workload and its data to another provider using the
  documented runbook?
- Who receives an alert, what do they do, and has that response been rehearsed?

## Claim boundary

Clearly label every statement as requirement, design, tested observation or
production result. A diagram, selected product, generated configuration or
small demonstrator is not evidence of scale, availability, compliance,
security or recovery.
