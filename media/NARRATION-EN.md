# English main narration

## 1 · The question

What does it actually mean to own a digital service? Not merely paying a
provider or having an account, but being able to inspect the source, understand
the identity boundary, make a verifiable backup and move the service when you
need to.

We built a complete small demonstrator over a few focused days. It is open
source, runs locally with synthetic data and answers one concrete question:
can the service leave target A and operate on target B without asking you to
trust a promise?

## 2 · What is inside

The demo combines a small notes application, PostgreSQL data, real Keycloak
OIDC identity, role-based access, a structured audit trail and encrypted Restic
backups. Container images are pinned to exact digests and Python dependencies
are hash locked.

That does not make it an enterprise platform. It makes each important part of
the demonstration visible, buildable and testable by someone else.

## 3 · Identity that really rejects

A security test is more than a successful login. We also tested what must be
stopped. A request without a token was rejected. A token issued for the wrong
audience was rejected. A normal user could not enter the administrator audit
view. And an account still required to enrol TOTP could not bypass that step.

Valid user and administrator access succeeded. Audit events retain the action,
outcome, target and a short subject hash—not passwords, bearer tokens or the
body of a note.

## 4 · The exit rehearsal

We first created two entirely synthetic records on target A. We stopped and
restarted A to prove ordinary persistence. Record count and the deterministic
SHA-256 state fingerprint remained identical.

Next, the PostgreSQL export received a checksum, entered an encrypted Restic
repository and passed Restic's integrity check.

Then came the essential boundary: target A's application and database were
stopped before target B could be accepted. The backup was restored into B's
separate database and the same access controls were tested again.

The result was two out of two records with the exact same content hash. The
complete application and data exit took 24.843 seconds in this small run. The
backup part took 6.457 seconds. Sampled aggregate peak memory was about 665
MiB.

Those are observations from one synthetic demo on one host. They are not a
production capacity, uptime or performance promise.

## 5 · What we do not hide

The identity provider remained shared during the exit. We therefore do not
call this a measured identity migration. Moving identity for real involves a
new trusted issuer, key rotation, client changes and usually re-enrolment of
strong authentication.

Keycloak also runs in development mode with a small embedded store. The demo
does not include high availability, public TLS, production monitoring or a
certification. Its purpose is to teach and prove a bounded process—not conceal
the work between a lab and an operated service.

The same honesty applies to physical technology. RFID cards, fingerprint
readers, WebAuthn keys and other access components can be considered as later
upgrades. No physical card was ordered, integrated or tested in this release.

## 6 · Why open source

With open source, the value is not a secret ZIP file. The value is knowing how
to adapt the environment, integrate company systems, choose the right security
boundaries and rehearse recovery before it becomes urgent.

You can clone the project from GitHub or GitLab, inspect every file and run the
whole rehearsal yourself. Secrets are generated locally and never enter Git.
When the test is complete, every demo container is stopped, while the small
practice volumes can remain for the next session.

## 7 · How a company can use it

A company with its own technical team can use the framework for internal
training and continue independently. A company that wants help can decide
where our expertise enters: assessment, secure architecture, integration,
documentation, a complete handover or continued operation.

Often the most sustainable answer is to upgrade the component that has become
obsolete, not discard everything. You can choose the hardware that fits. We
can help make the digital integrations, tests and future path real.

## 8 · Close

This project does not claim that every cloud is simple. It shows that ownership
can be made concrete: source you can read, data you can export, backups you can
verify and an exit you can repeat.

Inspect the open source. Read the machine-verifiable evidence. Run the small
demo yourself. And if you want to apply the principle inside your company,
contact IntentForce.
