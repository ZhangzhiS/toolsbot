from fastapi import FastAPI, APIRouter
import nonebot
from .api.wechat import wx_bot


driver = nonebot.get_driver()

BaseApiRouter = APIRouter(prefix="/api")

BaseApiRouter.include_router(wx_bot)


@driver.on_startup
async def _():
    app: FastAPI = nonebot.get_app()
    app.include_router(BaseApiRouter)

