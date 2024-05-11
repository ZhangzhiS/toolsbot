from arclet.alconna import Alconna, Args, Option, Subcommand
from nonebot import get_plugin_config, on_keyword
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from .config import Config
from toolsbot.adapters.wechat.event import Event
from toolsbot.adapters.wechat.message import SendTextMessage

__plugin_meta__ = PluginMetadata(
    name="helper",
    description="功能查询",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

cmd_parse = Alconna("帮助", Args["command", str | None])
cmd_parse.shortcut(r"^帮助 (?P<command>.+)$", {"args": ["{command}"], "fuzzy": False})
cmd_parse.shortcut(r"^help (?P<command>.+)$", {"args": ["{command}"], "fuzzy": False})

helper = on_keyword(
    {
        "帮助",
    },
    priority=1,
    rule=to_me(),
)


@helper.handle()
async def _(event: Event, matcher: Matcher):
    params = cmd_parse.parse(event.content)
    if not params.matched:
        return
    matcher.stop_propagation()
    cmd = params.main_args.get("command")
    if not cmd:
        msg = SendTextMessage(f"""帮助：
返利：私聊发送链接给我，通过转链链接下单，订单完成可以获得返利
天气：发送城市名称，可以获取天气预报
""")
        await helper.finish(msg)
