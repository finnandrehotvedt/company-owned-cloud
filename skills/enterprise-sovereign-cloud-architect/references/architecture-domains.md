# Architecture domains

Use these domains together. A decision in one domain must name its effect on
the others.

## Business and enterprise architecture

- Map business services to workloads, owners, criticality and data classes.
- Separate shared, dedicated and isolated infrastructure deliberately.
- Model expected users, tenants, transactions, growth and maintenance windows.
- Define which services may degrade and which must continue during failure.

## Sovereignty and external dependency

Answer for each platform layer:

- Who owns or leases the hardware?
- Who can technically access it?
- Who controls encryption keys and root identities?
- Where is each data class stored, replicated and backed up?
- Which external service is required for startup, login, operation or recovery?
- Can the service continue safely when that dependency is unavailable?
- Can the company migrate away with source, configuration, data and identity?

Sovereignty is verifiable control and exit capability, not merely a local
server or national address.

## Compute and application platform

- Consider dedicated Linux, virtual machines, containers, Proxmox, OpenStack
  and Kubernetes according to scale and operator capability.
- Define scheduling, workload placement, resource limits, image provenance,
  upgrades and rollback.
- Keep state outside disposable compute where practical.
- Provide a governed path for company applications, APIs, portals, databases,
  automations and new internally developed tools.

## Availability and resilience

- Remove or explicitly accept single points of failure across power, host,
  storage, network, database, identity, DNS, secrets and operators.
- Define failover trigger, authority, data-loss window and failback.
- Distinguish high availability from disaster recovery.
- Test component loss, site loss and dependency loss independently.

## Tenant isolation

Each tenant boundary must cover network, compute, storage, identity,
credentials, encryption context, logs, backup, quotas and administrative
access. Prove both data isolation and control-plane isolation with negative
tests. Shared observability must not leak tenant payloads or secrets.

## Security and Zero Trust

- Use least privilege, RBAC, MFA, workload identities, protected secrets,
  certificate lifecycle, segmentation, firewall policy and audit logging.
- Define administrative planes separately from service traffic.
- Model compromise, credential theft, insider access and supply-chain risk.
- Make emergency access time-bounded, logged and recoverable.

## Infrastructure as code and delivery

- Use versioned declarative configuration such as OpenTofu/Terraform, Ansible,
  Git and policy checks where they fit.
- Rebuild from documentation, code and protected secret sources.
- Require review, automated validation, staged rollout and scoped rollback.
- Detect configuration drift instead of relying on undocumented manual state.

## Observability and SRE

- Cover metrics, logs, traces, health checks, capacity and synthetic service
  probes.
- Define SLI/SLO and alert ownership before promising SLA.
- Minimise sensitive content in telemetry and set retention deliberately.
- Connect alerts to a tested operator action or safe automation.

## Backup and disaster recovery

- Define RPO/RTO per service and data class.
- Use protected off-site and, where appropriate, immutable copies.
- Include databases, configuration, identity, keys and dependency metadata.
- Record restore prerequisites and test restores into isolated targets.
- A successful backup job is not a successful recovery test.

## Enterprise networking

- Design address ownership, VLAN/VXLAN/SDN segmentation, routing, DNS,
  firewall zones, ingress, egress, VPN/WireGuard/IPsec, load balancing and
  out-of-band management.
- Use diverse paths only when physical and provider diversity are real.
- Define how independent data-centre locations connect and fail safely.

## Identity and access

- Integrate or isolate Entra ID, Active Directory, LDAP, Keycloak, OIDC, OAuth2
  and SAML based on the business boundary.
- Cover joiner/mover/leaver lifecycle, machine identities, federation failure,
  MFA recovery and break-glass access.
- Do not call an application/data move complete if identity remains an
  undocumented, non-portable dependency.

## Data governance

- Record physical location, classification, owner, lawful retention, deletion,
  access, encryption and audit trail.
- Separate operational access from business-data access.
- Verify deletion and export paths, including replicas and backups.
