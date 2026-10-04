# Identity and MFA

Keycloak 26.3.3 is the real local OIDC provider. The repository declares two
realm roles, `cloud-user` and `cloud-admin`, and two public lab clients used to
prove correct and incorrect audience handling.

`scripts/bootstrap_identity.py` creates three synthetic users idempotently:

- an automation user with `cloud-user`;
- an audit administrator with both roles;
- an `mfa-pending` user with `CONFIGURE_TOTP` required.

The acceptance test proves that the first two receive valid tokens and that
the MFA-pending user's password grant fails closed. It does not claim that a
human TOTP ceremony was automated.

To rehearse real enrolment locally, run `scripts/labctl start-a`, open the
Keycloak account page at
`http://127.0.0.1:18790/realms/company-owned-cloud/account/`, and sign in as
`mfa-pending`. The generated password exists only in
`runtime/secrets/mfa_pending_password`; reading it is an explicit local
operator action. Follow the QR-code flow with an authenticator, sign out and
sign in again. Do not reuse this lab identity or its credentials in production.

A real migration must export identities with an approved format, establish a
new trusted issuer, rotate client configuration and keys, test recovery codes,
and normally require users to re-enrol phishing-resistant MFA. None of that is
counted as measured in this demo.
