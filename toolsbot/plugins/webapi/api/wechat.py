from fastapi import APIRouter, Request
from nonebot import get_bots, logger

from toolsbot.adapters.wechat.bot import Bot
from models.bot import WeChatBot
from toolsbot.plugins.webapi.api.params import CreateWeChatBot
from toolsbot.utils.auth import get_code

wx_bot_route = APIRouter(prefix="/wx")


@wx_bot_route.get("/test")
def get():
    return {"success": True}


@wx_bot_route.get("/bots")
async def _(request: Request):
    user_id = request.state.user_id
    query = {"user_id": user_id}
    bots = await WeChatBot.get_bots()
    return bots

@wx_bot_route.post("/bot")
async def _(wx_bot_info: CreateWeChatBot, request: Request):
    code = get_code(wx_bot_info.wxid, wx_bot_info.callback_url)
    wx_bot_info.code = code
    wx_bot_info.user_id = request.state.user_id
    item = await WeChatBot.create_or_update_bot(wx_bot_info)
    return item

    
@wx_bot_route.post("/bot/update")
async def _(params: CreateWeChatBot):
    pass
