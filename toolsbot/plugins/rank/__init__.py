from nonebot import on_keyword
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from toolsbot.adapters.wechat.event import Event
from arclet.alconna import Alconna, Args

from toolsbot.adapters.wechat.message import SendTextMessage

__plugin_meta__ = PluginMetadata(
    name="奋斗逼计数器",
    description="看看谁是奋斗逼",
    usage="",
)


rank = on_keyword(
    {
        "rank",
    },
    rule=to_me(),
)

cmd_parse = Alconna("rank", Args["option", str])
cmd_parse.shortcut(r"^(?P<option>.+) rank$", {"args": ["{option}"], "fuzzy": False})
cmd_parse.shortcut(r"^rank (?P<option>.+)$", {"args": ["{option}"], "fuzzy": False})


@rank.handle()
async def _(event: Event, matcher: Matcher):
    room_id = "19790302666@chatroom"
    if event.roomid != room_id:
        msg = SendTextMessage("本群暂不支持!")
        return await rank.finish(msg, receiver=room_id)
    params = cmd_parse.parse(event.content)
    if not params.matched:
        return

    matcher.stop_propagation()

    option = params.main_args.get("option", "")

    if not option:
        option = "day"

    msg = SendTextMessage(option)
    await rank.send(msg)

