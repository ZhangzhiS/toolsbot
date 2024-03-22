from fastapi import APIRouter
from nonebot import get_bots, logger

from toolsbot.adapters.wechat.bot import Bot

wx_bot = APIRouter(prefix="/wx")


@wx_bot.get("/test")
def get():
    return {"success": True}


@wx_bot.get("/bots")
async def _():
    bots: Bot = get_bots()
    logger.error(bots)
    res = []
    for bot_id in bots:
        bot = bots[bot_id]
        if bot.type == "WeChat":
            logger.error(bot)
            res.append(bot.wx_config.model_dump())
    return res
