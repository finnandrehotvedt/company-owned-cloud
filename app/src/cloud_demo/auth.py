from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient


ISSUER = os.environ["OIDC_ISSUER"]
JWKS_URL = os.environ["OIDC_JWKS_URL"]
AUDIENCE = os.environ["OIDC_AUDIENCE"]

bearer = HTTPBearer(auto_error=False)
jwks = PyJWKClient(JWKS_URL, cache_keys=True, lifespan=300)


@dataclass(frozen=True)
class Principal:
    subject: str
    username: str
    roles: frozenset[str]


def authenticate(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> Principal:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="bearer token required")
    token = credentials.credentials
    try:
        signing_key = jwks.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=ISSUER,
            options={"require": ["exp", "iat", "iss", "sub", "aud"]},
        )
    except Exception as error:  # PyJWT exposes several verification subclasses.
        request.state.auth_failure = type(error).__name__
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token rejected") from None
    roles = frozenset(payload.get("realm_access", {}).get("roles", []))
    return Principal(
        subject=str(payload["sub"]),
        username=str(payload.get("preferred_username", "unknown")),
        roles=roles,
    )


def require_role(role: str) -> Callable[[Principal], Principal]:
    def dependency(principal: Principal = Depends(authenticate)) -> Principal:
        if role not in principal.roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="role required")
        return principal

    return dependency


cloud_user = require_role("cloud-user")
cloud_admin = require_role("cloud-admin")
