# Working memory

- Updated: 4 October 2026 Europe/Oslo
- Scope: `desktop-owned-cloud-publication-20261004-001`
- Current state: project root and small-demo specification established on
  CT109 after role and live-capacity verification.
- Verified capacity: 10 CPUs, 12 GiB RAM / 9 GiB available, 7.3 GiB disk free;
  Docker 20.10.24 and standalone docker-compose 1.29.2.
- Decision: maximum demo budget below 2 CPUs, 2 GiB RAM and 2.5 GiB new disk;
  loopback ports 18780/18781/18790; final state stopped.
- Boundaries: synthetic data only; no production/client migration, public
  runtime, paid infrastructure, HA or enterprise-ready claim.
- Next action: implement the pinned Compose lab, tests, backup/restore and
  measured A-to-B exit, then publish only after evidence is green.
- Blockers: none currently. Public repository credentials and website release
  routes must be verified locally before use without exposing them.
