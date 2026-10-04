# Known limitations

- Small single-host synthetic demonstrator only.
- No public runtime, TLS, HA, SLA or production support claim.
- Shared Keycloak identity is not moved during the measured A-to-B exit.
- Keycloak `start-dev` uses an embedded lab store and starts slowly under the
  deliberate 0.4 CPU limit.
- CT109 uses host-loopback networking due its existing Docker network state;
  portability to another host still requires the preflight checks.
- Direct password grants exist solely for repeatable local negative/positive
  tests; production clients should use suitable interactive/service flows.
- Peak memory is sampled once per second and is a demo observation, not a
  capacity benchmark.
- No physical access card, fingerprint reader or device SDK is included or
  tested.
