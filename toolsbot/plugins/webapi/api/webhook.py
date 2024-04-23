# import time
from urllib.parse import urljoin

import httpx
from fastapi import APIRouter
from fastapi.requests import Request
from nonebot import get_driver, logger

from models.bot import WeChatBot
from models.webhook import WebhookAuth
from toolsbot.adapters.wechat.api import SendTextMessageAPI
from toolsbot.utils.auth import decode_info, encode_info

from .params import CreateWebHookParams, WebHookParams

utils_route = APIRouter(prefix="/wh")
config = get_driver().config


@utils_route.get("/token/list")
async def get_push_token_list(request: Request):
    """
    获取调用推送的 code 列表
    """
    user_id = request.state.user_id
    if not user_id:
        return {"success": False}
    codes = await WebhookAuth.filter(user_id=user_id)
    res = []
    for code in codes:
        tmp = decode_info(code.token)
        tmp["token"] = code.token
        tmp["token_id"] = str(code.id)
        res.append(tmp)
    return res


@utils_route.post("/token/create")
async def create_push_token(info: CreateWebHookParams, request: Request):
    """
    创建推送的 code
    """
    user_id = request.state.user_id
    code = encode_info(info.model_dump())
    bot = await WeChatBot.get_or_none(wxid=info.bot_id)
    if not bot:
        return {"success": False, "msg": "机器人不存在"}
    remark = f"使用 {bot.name} -> {info.receiver_name}"
    await WebhookAuth.create(
        user_id=user_id, token=code, bot_type=info.bot_type, remark=remark
    )
    return {"success": True}


@utils_route.post("/token/delete/{token_id}")
async def delete_push_token(token_id: str):
    """
    删除推送的 code
    """
    code = await WebhookAuth.get_or_none(id=token_id)
    if not code:
        return {"success": False}
    await code.delete()
    return {"success": True}


@utils_route.post("/push")
async def push_to_wechat(r: WebHookParams):
    """
    推送到机器人
    """
    receiver_info = [decode_info(i) for i in r.tokens]
    bots = await WeChatBot.filter(wxid__in=[i["bot_id"] for i in receiver_info])
    bots = {i.wxid: i for i in bots}
    async with httpx.AsyncClient() as client:
        for receiver in receiver_info:
            print(receiver)
            callback_url = bots[receiver["bot_id"]].callback_url
            data = {"receiver": receiver["receiver"], "msg": r.msg, "aters": ""}
            api = urljoin(callback_url, SendTextMessageAPI().api)
            try:
                logger.info(f"""
                push api {api}
                data {data}
                """)
                await client.post(api, json=data)
            except Exception as e:
                logger.info(f"推送到 {receiver['receiver_name']} 失败 {e}")
    return {"success": True}
