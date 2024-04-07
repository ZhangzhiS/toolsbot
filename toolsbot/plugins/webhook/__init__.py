from nonebot import get_plugin_config, on_notice
from nonebot.plugin import PluginMetadata

from .config import Config
from toolsbot.adapters.wechat.event import Event

__plugin_meta__ = PluginMetadata(
    name="webhook",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

wh = on_notice()


@wh.handle()
async def _(event: Event):
    msg = event.content
    await wh.finish(msg)
