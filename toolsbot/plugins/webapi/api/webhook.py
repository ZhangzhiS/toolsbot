import time
from typing import Optional

import httpx
from fastapi import APIRouter
from nonebot import get_driver
from pydantic import BaseModel

from models.webhook import WebhookAuth

utils_route = APIRouter(prefix="/wh")
config = get_driver().config


class WebHookParams(BaseModel):
    token: str
    title: str
    content: Optional[str]


@utils_route.post("/bot")
async def push_to_wechat(r: WebHookParams):
    """
    推送到机器人
    """
    if not await WebhookAuth.exists(token=r.token):
        return {"success": False}
    msg = r.title
    if r.content:
        msg = f"{r.title}\n----------------\n{r.content}"
    # if r.receiver is None:
    #     r.receiver = ""
    # buile_callback_data = dict(
    #     is_self=False,
    #     is_group=False,
    #     id=6666,
    #     ts=time.time(),
    #     room_id="",
    #     content=msg,
    #     sender=r.receiver,
    #     sign="",
    #     thumb="",
    #     extra="",
    #     xml="",
    # )
    # async with httpx.AsyncClient() as client:
    #     params = dict(
    #         code="d3hpZF9seXhxN2hub3k4ZDQyMnxodHRwOi8vMTkyLjE2OC42OC4xMTE6MTAwMTAv"
    #     )
    #     response = await client.post(
    #         f"http://localhost:{config.port}/wechat/callback",
    #         params=params,
    #         data=buile_callback_data,
    #     )
    #     return response.json()
