from fastapi import FastAPI, APIRouter
import nonebot
from .api.wechat import wx_bot_route
from .core.middleware import LogtoAuthMiddleware


driver = nonebot.get_driver()

BaseApiRouter = APIRouter(prefix="/api")

BaseApiRouter.include_router(wx_bot_route)

app: FastAPI = nonebot.get_app()

# 中间件
app.add_middleware(LogtoAuthMiddleware)

@driver.on_startup
async def _():
    # app: FastAPI = nonebot.get_app()
    # 路由
    app.include_router(BaseApiRouter)

