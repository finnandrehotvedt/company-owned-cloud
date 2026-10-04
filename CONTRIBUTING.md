# Contributing

Issues and focused pull requests are welcome. Keep changes inside the small
synthetic-demo boundary, add or update tests, and never commit runtime secrets,
tokens, real user data or production topology.

Before proposing a change, run:

```sh
scripts/labctl validate
scripts/verify_release.py
```

Changes to authentication, export/restore order, listener addresses, secret
handling or evidence claims should also rerun `scripts/labctl integration` and
explain any changed measurement. Physical credential support requires a new,
separately approved hardware/security scope.
