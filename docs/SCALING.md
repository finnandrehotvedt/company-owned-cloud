# Scaling beyond the demonstrator

The measured repository is intentionally small. A production engagement would
begin with requirements and a threat model, then separately design:

- external TLS termination and private service networking;
- production-grade identity/database clusters and protected key custody;
- off-site immutable backups and regularly witnessed disaster recovery;
- observability, patch ownership, incident response and operator coverage;
- load/capacity testing, availability objectives and compliance evidence;
- tenant/data classification and an approved migration/rollback plan.

These are roadmap items, not evidence supplied by this repository.

Optional later upgrades can include WebAuthn security keys, RFID/smart-card
readers, fingerprint-enabled credentials or other building/access technology.
Each requires hardware selection, SDK/protocol review, privacy assessment,
fallback procedures and an independent security test. This project does not
order or recommend a specific physical card.
