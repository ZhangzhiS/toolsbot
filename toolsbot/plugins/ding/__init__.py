
# from nonebot.params import Command
from nonebot.plugin import PluginMetadata
from nonebot import logger, on_keyword
from nonebot.rule import to_me
from toolsbot.adapters.wechat.api import SendTextMessageAPI
from toolsbot.adapters.wechat.event import Event
from toolsbot.adapters.wechat.message import SendTextMessage, MessageSegment


__plugin_meta__ = PluginMetadata(
    name="叮咚测试",
    description="叮咚测试，测试适配器功能",
    usage="",
)


wxid = on_keyword(
    {
        "ding",
    },
    rule=to_me(),
)


@wxid.handle()
async def _():
    msg = SendTextMessage("dong")
    await wxid.send(msg)
