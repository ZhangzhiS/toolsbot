from nonebot import get_bots
from fastapi import APIRouter

from toolsbot.adapters.wechat.bot import Bot

wx_bot = APIRouter(prefix="/wx")


@wx_bot.get("/test")
def get():
    return {"success": True}


@wx_bot.get("/bots")
async def _():
    bots: Bot = get_bots()
    res = []
    for bot in bots:
        print(bot)
    return res
