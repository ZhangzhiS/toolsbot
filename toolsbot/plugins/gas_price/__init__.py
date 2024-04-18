from arclet.alconna import Alconna, Args
from nonebot import get_plugin_config, on_keyword
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from .config import Config

__plugin_meta__ = PluginMetadata(
    name=" 油价查询",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

gas_price = on_keyword(
    {
        "gas",
    },
    block=True,
    priority=1,
    rule=to_me(),
)

cmd_parse = Alconna("天气", Args["city", str])
cmd_parse.shortcut(r"^(?P<city>.+)天气$", {"args": ["{city}"], "fuzzy": False})
cmd_parse.shortcut(r"^天气(?P<city>.+)$", {"args": ["{city}"], "fuzzy": False})


@gas_price.handle()
def _():
    pass
