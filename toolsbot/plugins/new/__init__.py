
# from nonebot.params import Command
from nonebot.plugin import PluginMetadata
from nonebot import on_keyword
from nonebot.rule import to_me


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
    await wxid.send("dong")
