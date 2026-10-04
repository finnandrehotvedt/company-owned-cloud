# English short film · under 3 minutes

What does it mean to own a digital service? We chose to answer with a test, not
a slogan.

Over a few focused days we built a complete small open-source demonstrator: a
notes service, PostgreSQL, real Keycloak OIDC, roles, a content-minimised audit
trail and encrypted Restic backup.

First we tested identity. Valid user and administrator access worked. A missing
token, wrong audience, insufficient role and an account still required to
enrol TOTP were all rejected.

Then we placed two synthetic records on target A. After a full restart, record
count and the SHA-256 state fingerprint were unchanged.

The data was exported, checksummed and placed in an encrypted backup. We then
stopped both the application and database on A before B could be accepted. On
B we restored the database, repeated the access checks and compared state.

Two out of two records. The exact same content hash. Backup took 6.457 seconds,
and the complete application and data exit took 24.843 seconds. Sampled peak
memory was about 665 MiB.

This is a small measured demo—not a production platform or capacity promise.
The identity provider remained shared and was not migrated. No physical RFID
or fingerprint card was ordered or tested; those are only examples of future
upgrades.

All source and machine-readable evidence are public on GitHub and GitLab. Run
the exercise yourself, learn from it and extend it. Or choose where IntentForce
should help: integration, security, training, handover or continued operation.

Ownership becomes real when you can read the source, verify the backup and
prove that the service can leave.
