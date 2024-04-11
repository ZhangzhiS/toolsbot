import httpx
from jose import jwt
from nonebot import get_plugin_config, logger
from pydantic import BaseModel
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from starlette.middleware.base import BaseHTTPMiddleware


class LogtoConfit(BaseModel):
    logto_jwks_url: str
    logto_issuer: str


config = get_plugin_config(LogtoConfit)


async def fetch_jwks_uri():
    async with httpx.AsyncClient() as client:
        response = await client.get(config.logto_jwks_url)
        return response.json()


def write_not_authed(msg: str = "未授权"):
    response = {"msg": msg, "success": 0}
    return JSONResponse(content=response, status_code=401)


class LogtoAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        whitelist = ["/wechat/callback"]
        if request.url.path in whitelist:
            return await call_next(request)
        auth = request.headers.get("Authorization")
        if not auth:
            return write_not_authed()
        content = auth.split()
        if len(content) < 2:
            return write_not_authed("token error")
        elif content[0] != "Bearer":
            return write_not_authed("token type not support")
        token = content[1]
        jwks = await fetch_jwks_uri()
        try:
            payload = jwt.decode(
                token,
                jwks,
                algorithms=jwt.get_unverified_header(token).get("alg"),
                audience="http://127.0.0.1:8080",
                issuer=config.logto_issuer,
                options={"verify_at_hash": False},
            )
        except Exception as e:
            return write_not_authed(str(e))

        request.state.user_id = payload.get("sub")
        response = await call_next(request)
        return response
