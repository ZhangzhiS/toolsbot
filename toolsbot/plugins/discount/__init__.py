from nonebot import get_plugin_config, logger, on_keyword
from nonebot.plugin import PluginMetadata

from toolsbot.adapters.wechat.api import SendTextMessage
from toolsbot.adapters.wechat.event import Event
from toolsbot.utils.dtk import dtk_cli
from toolsbot.adapters.wechat import model
from toolsbot.adapters.wechat.api import SendTextMessage

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="折扣信息",
    description="处理收到的折扣信息",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

forward_plugin = on_keyword({"u.jd.com"}, block=True)


@forward_plugin.handle()
async def _(event: Event):
    if event.roomid != "22374012632@chatroom":
        return
    if event.sender != "wxid_hdo76qijifvz22":
        return
    return await forward_plugin.send(
        "",
        wx_ctrl=SendTextMessage.model_validate(
            dict(post_data={"receiver": "34407719097@chatroom", "msg": event.content, "aters": ""})
        )
    )
