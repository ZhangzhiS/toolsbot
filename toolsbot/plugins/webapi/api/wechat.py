from typing import Optional
from urllib.parse import urljoin

import httpx
from fastapi import APIRouter, Request
from nonebot import logger

from models.bot import WeChatBot, WeChatBotContact
from toolsbot.adapters.wechat.api import GetWeChatContactAPI
from toolsbot.plugins.webapi.api.params import CreateWeChatBot, DeleteWeChatBotParams
from toolsbot.utils.auth import encode_info

wx_bot_route = APIRouter(prefix="/wx")


@wx_bot_route.get("/test")
def get():
    return {"success": True}


@wx_bot_route.get("/bot/list")
async def _(request: Request):
    user_id = request.state.user_id
    bots = await WeChatBot.filter(user_id=user_id)
    return bots


@wx_bot_route.post("/bot/create")
async def create_bot(wx_bot_info: CreateWeChatBot, request: Request):
    bot = await WeChatBot.get_or_none(wxid=wx_bot_info.wxid)
    encode_dict = {
        "wxid": wx_bot_info.wxid,
        "callback_url": wx_bot_info.callback_url,
        "name": wx_bot_info.name,
    }
    code = encode_info(encode_dict)
    insert_info = wx_bot_info.model_dump()
    insert_info["code"] = code
    insert_info["user_id"] = request.state.user_id
    if bot:
        bot.update_from_dict(insert_info)
    else:
        bot = WeChatBot(**insert_info)
    await bot.save()
    return bot


@wx_bot_route.post("/bot/del")
async def delete_bot(wxid: DeleteWeChatBotParams):
    bot = await WeChatBot.get_or_none(wxid=wxid.wxid)
    logger.info(f"delete bot {bot}")
    if not bot:
        return {"success": False, "msg": "bot not found"}
    bot.status = False
    await bot.save()
    return {"success": True}


@wx_bot_route.get("/contact")
async def get_contacts(bot_id: Optional[str] = None):
    """
    获取联系人列表
    """
    if bot_id:
        contacts = await WeChatBotContact.filter(bot_id=bot_id)
    else:
        contacts = await WeChatBotContact.all()
    return contacts


@wx_bot_route.get("/contact/refresh")
async def refresh_contacts(bot_id: str):
    """
    获取联系人列表
    增量添加，不刷新旧数据，联系人修改昵称这里不刷新
    """
    bot = await WeChatBot.get_or_none(wxid=bot_id)
    if not bot:
        return {"success": False, "msg": "bot not found"}
    contact_url = urljoin(bot.callback_url, GetWeChatContactAPI.api)
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url=contact_url)
        except Exception as e:
            return {"success": False, "msg": f"{e}"}
    contacts = resp.json().get("data", {}).get("contacts", [])
    wxids = {contact["wxid"]: contact for contact in contacts}
    indb_contacts = await WeChatBotContact.filter(bot_id=bot_id).in_bulk(wxids, "wxid")
    not_indb_contacts = [
        contact for contact in contacts if contact["wxid"] not in indb_contacts
    ]
    insert_users = []
    for contact in not_indb_contacts:
        contact["bot_id"] = bot_id
        insert_users.append(WeChatBotContact(**contact))
    await WeChatBotContact.bulk_create(insert_users)
    return {"success": True}
