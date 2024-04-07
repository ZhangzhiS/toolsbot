import asyncio
from typing import Optional
from fastapi import APIRouter
from nonebot import get_bot, logger
from pydantic import BaseModel

from toolsbot.adapters.wechat.bot import Bot

utils_route = APIRouter(prefix="/wh")


class WebHookParams(BaseModel):
    token: str
    title: str
    content: Optional[str]
    sender: str
    receiver: str


@utils_route.post("/wechat")
async def push_to_wechat(r: WebHookParams):
    local_token = "pushtoken"
    if r.token != local_token:
        return {"success": False}
    msg = r.title
    if r.content:
        msg = f"{r.title}\n----------------\n{r.content}"
    try:
        bot = get_bot(r.sender)
    except KeyError:
        logger.warning(f'No bot with specific id: {r.sender}')
        return
    except ValueError:
        logger.warning('No bot available or driver not initialized')
        return
    if r.receiver is None:
        r.receiver = ""
    await bot.send("", msg)
