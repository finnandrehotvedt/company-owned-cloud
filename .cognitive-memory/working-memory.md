# Working memory

- Updated: 4 October 2026 Europe/Oslo
- Scope: `desktop-owned-cloud-publication-20261004-001`
- Current state: complete local small-demo implementation and measured A-to-B
  exit are green; runtime is stopped. GitHub/GitLab and the public evidence page
  are live. The additive Enterprise Sovereign Cloud architecture framework and
  reusable agent skill are being prepared for the same public mirrors.
- Verified capacity: 10 CPUs, 12 GiB RAM / 9 GiB available, 7.3 GiB disk free;
  Docker 20.10.24 and standalone docker-compose 1.29.2.
- Decision: maximum demo budget below 2 CPUs, 2 GiB RAM and 2.5 GiB new disk;
  host-loopback ports 18780/18781/18782/18783/18790 after CT109 bridge traffic
  failed without shared-firewall changes; final state stopped.
- Boundaries: synthetic data only; no production/client migration, public
  runtime, paid infrastructure, HA or enterprise-ready claim.
- Evidence: 2 synthetic records; exact content hash match; positive and four
  negative identity/role cases passed; backup 6.457 seconds; complete measured
  application/data exit 24.843 seconds; sampled aggregate peak memory
  697,502,266 bytes; identity exit unmeasured; physical cards not tested.
- Runtime verification: no project containers or reserved-port listeners after
  integration; volumes retained; source/runtime secrets excluded from Git.
- New framework: `docs/ENTERPRISE-SOVEREIGN-CLOUD.md` presents dedicated Linux
  servers, selected data centres, applications, identity, security,
  observability, recovery, tenant isolation and exit as one platform. The
  reusable skill is `skills/enterprise-sovereign-cloud-architect/`.
- Claim boundary: the new material is architecture guidance and a roadmap. It
  does not change or expand the measured single-host demo evidence.
- Next action: validate and publish one identical framework/skill commit to
  GitHub and GitLab, then release the matching website positioning update.
- Blockers: none currently.
