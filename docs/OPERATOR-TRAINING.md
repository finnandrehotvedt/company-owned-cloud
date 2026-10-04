# Operator training exercise

1. Read `SPECIFICATION.md`, then predict which negative identity tests should
   fail and why.
2. Run `scripts/labctl integration` with synthetic data only.
3. Inspect `evidence/measured-2026-10-04/summary.json` and explain the difference
   between a matching content hash and a complete disaster-recovery proof.
4. Locate the exact point where target A is stopped before target B is
   accepted.
5. Practise ordinary `stop` and start without deleting volumes.
6. Discuss the unmeasured identity migration and write a rehearsal plan before
   proposing any production use.

Approval buttons or dashboards can be added later, but the source-controlled
runbook remains the canonical process. Operators should be able to explain and
repeat every state transition without relying on a hidden service.
