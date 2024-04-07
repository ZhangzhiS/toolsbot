from nonebot import get_plugin_config, logger, on_keyword
from nonebot.plugin import PluginMetadata

from toolsbot.adapters.wechat.event import Event
from toolsbot.utils.dtk import dtk_cli
from toolsbot.adapters.wechat.api import SendTextMessageAPI

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
    res = await dtk_cli.get_jd_url_content(event.content)
    if res:
        return await forward_plugin.send(
            "",
            wx_ctrl=SendTextMessageAPI.model_validate(
                dict(
                    post_data={
                        "receiver": "34407719097@chatroom",
                        "msg": event.content,
                        "aters": "",
                    }
                )
            ),
        )
