import json
from logging import getLogger

import jwt
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import Response

http_bearer = HTTPBearer()
log = getLogger(__name__)


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Starlette Middleware class to handle JWT Authentication and Authorization."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Default Middleware gateway required by Starlette."""
        with open("settings.json") as f:
            if not (jwt_secret := json.load(f).get("jwt_secret")):
                return JSONResponse(content={"msg": "Improperly configured JWT secret."}, status_code=500)
            if "Authorization" not in request.headers:
                return JSONResponse(content={"msg": "No Authorization header in request body"}, status_code=403)
            auth_header = request.headers["Authorization"]
            scheme, bearer = auth_header.split()
            if scheme.lower() != "bearer":
                return JSONResponse(content={"msg": "Invalid token scheme!"}, status_code=403)
            try:
                payload = jwt.decode(
                    bearer,
                    jwt_secret,
                    options={"verify_signature": True, "require": ["exp"], "verify_exp": True},
                    algorithms=["HS256"],
                )
            except jwt.DecodeError as exc:
                return JSONResponse(
                    content={
                        "msg": "Something went wrong authenticating your request, the signature verification failed."
                    },
                    status_code=403,
                )
            else:
                if payload["type"] == "deploy":
                    return await call_next(request)
                return JSONResponse(content={"msg": "Invalid type of token"}, status_code=403)
