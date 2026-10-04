from __future__ import annotations

import html
import os
import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .auth import Principal, cloud_admin, cloud_user
from .db import audit_safety, connection, migrate, state_summary, write_audit


TARGET = os.environ.get("DEMO_TARGET", "unknown")


@asynccontextmanager
async def lifespan(_: FastAPI):
    migrate()
    yield


app = FastAPI(
    title="Company-Owned Cloud Lab",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)


class NoteInput(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    body: str = Field(min_length=1, max_length=4000)


def request_id(request: Request) -> str:
    incoming = request.headers.get("x-request-id", "")
    return incoming if 0 < len(incoming) <= 80 and incoming.replace("-", "").isalnum() else str(uuid.uuid4())


@app.get("/healthz")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "company-owned-cloud", "target": TARGET}


@app.get("/readyz")
def ready() -> dict[str, str]:
    with connection() as database:
        database.execute("SELECT 1").fetchone()
    return {"status": "ready", "target": TARGET}


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    summary = state_summary()
    target = html.escape(TARGET)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Company-Owned Cloud Lab · {target}</title>
<style>
:root{{--ink:#17221d;--muted:#66736c;--paper:#f4f0e7;--green:#1d664a;--line:#c8d0c8;--card:#fffdf8}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,sans-serif}}
main{{max-width:1050px;margin:auto;padding:42px 22px 70px}}.eyebrow{{letter-spacing:.14em;text-transform:uppercase;color:var(--green);font-weight:750;font-size:.78rem}}
h1{{font:clamp(2.6rem,7vw,5.4rem)/.96 Georgia,serif;margin:.2em 0}}.lead{{font-size:1.18rem;max-width:720px;color:#35443d}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:30px 0}}article{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px;min-width:0}}
.metric{{font:2rem/1 Georgia,serif;color:var(--green)}}code{{overflow-wrap:anywhere}}.flow{{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:34px 0}}
.node{{background:#fff;border:1px solid var(--line);border-radius:999px;padding:9px 14px}}.arrow{{color:var(--muted)}}footer{{border-top:1px solid var(--line);padding-top:20px;color:var(--muted)}}
</style></head><body><main>
<p class="eyebrow">Open source · small measured demonstrator</p><h1>The service can leave.</h1>
<p class="lead">This loopback-only lab shows one synthetic application and database under company-controlled source, identity policy, audit logging and encrypted backup. It is a measured demo, not an enterprise cloud claim.</p>
<div class="grid"><article><p class="eyebrow">Active target</p><p class="metric">{target}</p><p>Target A and B use separate application and database networks.</p></article>
<article><p class="eyebrow">Synthetic records</p><p class="metric">{summary['record_count']}</p><p>Protected content is available only through a valid OIDC token and role.</p></article>
<article><p class="eyebrow">State fingerprint</p><p><code>{summary['content_sha256'][:16]}…</code></p><p>The complete hash is used to compare source and restored targets.</p></article></div>
<div class="flow"><span class="node">Keycloak OIDC</span><span class="arrow">→</span><span class="node">Protected app</span><span class="arrow">→</span><span class="node">PostgreSQL</span><span class="arrow">→</span><span class="node">Encrypted Restic backup</span></div>
<footer>Only health and this synthetic status page are public inside the local lab. Note data and audit summaries require roles. Final lab state: stopped.</footer>
</main></body></html>"""


@app.get("/api/whoami")
def whoami(principal: Principal = Depends(cloud_user)) -> dict[str, object]:
    return {"username": principal.username, "roles": sorted(principal.roles), "target": TARGET}


@app.get("/api/notes")
def list_notes(principal: Principal = Depends(cloud_user)) -> dict[str, object]:
    with connection() as database:
        notes = database.execute(
            "SELECT id, title, body, created_by, created_at FROM notes ORDER BY id"
        ).fetchall()
    return {"target": TARGET, "notes": notes, "requested_by": principal.username}


@app.post("/api/notes", status_code=status.HTTP_201_CREATED)
def create_note(note: NoteInput, request: Request, principal: Principal = Depends(cloud_user)) -> dict[str, object]:
    rid = request_id(request)
    try:
        with connection() as database:
            row = database.execute(
                "INSERT INTO notes(title, body, created_by) VALUES (%s, %s, %s) RETURNING id, title, created_by, created_at",
                (note.title, note.body, principal.subject),
            ).fetchone()
            database.commit()
        write_audit(rid, principal.subject, "note.create", "allowed", TARGET)
        return {"target": TARGET, "note": row, "request_id": rid}
    except Exception:
        write_audit(rid, principal.subject, "note.create", "failed", TARGET)
        raise HTTPException(status_code=500, detail="note could not be stored") from None


@app.get("/api/state")
def state(principal: Principal = Depends(cloud_user)) -> dict[str, object]:
    return {"target": TARGET, **state_summary(), "requested_by": principal.username}


@app.get("/api/admin/audit-summary")
def audit_summary(principal: Principal = Depends(cloud_admin)) -> dict[str, object]:
    with connection() as database:
        rows = database.execute(
            "SELECT action, outcome, count(*) AS count FROM audit_events GROUP BY action, outcome ORDER BY action, outcome"
        ).fetchall()
    return {"target": TARGET, "events": rows, "requested_by": principal.username}


@app.get("/api/admin/audit-safety")
def audit_safety_report(principal: Principal = Depends(cloud_admin)) -> dict[str, object]:
    return {"target": TARGET, **audit_safety(), "requested_by": principal.username}
