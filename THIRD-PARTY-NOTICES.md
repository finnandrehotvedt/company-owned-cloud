# Third-party components

The source written for this repository is Apache-2.0. Runtime dependencies keep
their own licences:

| Component | Pinned release | Licence/source |
|---|---:|---|
| Python | 3.13.7 slim-bookworm image | PSF licence; <https://github.com/docker-library/python> |
| PostgreSQL | 17.6 bookworm image | PostgreSQL licence; <https://www.postgresql.org/about/licence/> |
| Keycloak | 26.3.3 image | Apache-2.0; <https://github.com/keycloak/keycloak> |
| Restic | 0.18.1 image | BSD-2-Clause; <https://github.com/restic/restic> |
| FastAPI | pinned in `app/requirements.lock` | MIT |
| Uvicorn | pinned in `app/requirements.lock` | BSD-3-Clause |
| Psycopg | pinned in `app/requirements.lock` | LGPL-3.0-or-later with stated exceptions |
| PyJWT | pinned in `app/requirements.lock` | MIT |
| cryptography | transitive/pinned lock entry | Apache-2.0 OR BSD-3-Clause |
| HTTPX | pinned in `app/requirements.lock` | BSD-3-Clause |
| jsonschema | pinned in `app/requirements.lock` | MIT |
| PyYAML | pinned in `app/requirements.lock` | MIT |

The exact image digests are declared in `.env.example` and `compose.yaml`.
Base images include additional Debian/UBI/Alpine packages under their upstream
licences. Run the documented SBOM command before a formal downstream release;
this file is a practical inventory, not legal advice.
