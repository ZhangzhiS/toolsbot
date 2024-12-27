from arclet.alconna import Alconna, Args
from nonebot import get_plugin_config, on_keyword
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from toolsbot.adapters.wechat.event import Event
from toolsbot.adapters.wechat.message import SendTextMessage

from .config import Config
from .get_message import get_discount_help_msg, get_help_msg

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
        msg = SendTextMessage(get_help_msg())
        await helper.finish(msg)
    if cmd == "返利":
        msg = SendTextMessage(get_discount_help_msg())
        await helper.finish(msg)
