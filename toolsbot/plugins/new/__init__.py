from typing import Tuple
# from nonebot.params import Command
from nonebot.plugin import PluginMetadata
from nonebot import on_keyword
from nonebot import logger
from nonebot.rule import to_me

from toolsbot.adapters.wechat.event import MessageEvent
from toolsbot.adapters.wechat.bot import Bot

__plugin_meta__ = PluginMetadata(
    name="ttt",
    description="",
    usage="",
)


wxid = on_keyword({"测试",}, rule=to_me())


@wxid.handle()
async def _():
    # _, action = cmd
    logger.debug(f"event.get_event_name() | {1}")
    await wxid.send("123123123")

