from typing import TYPE_CHECKING, Any, Optional, Union

from nonebot import logger
from nonebot.adapters import Bot as BaseBot
from nonebot.adapters import Event
from nonebot.adapters import (
    Message,
)
from nonebot.adapters import (
    MessageSegment,
)
from nonebot.message import handle_event
from typing_extensions import override

from toolsbot.adapters.wechat.api import WechatHookApi

from .config import Config
# from .event import Event
# from .message import Message, MessageSegment

if TYPE_CHECKING:
    from .adapter import Adapter


class Bot(BaseBot):
    def __init__(self, adapter: "Adapter", self_id: str, config: Config):
        super().__init__(adapter, self_id)
        self.wx_config: Config = config

    @override
    async def send(
        self,
        event: "Event",
        message: Union[str, "Message", "MessageSegment"],
        **kwargs: Any,
    ) -> Any:
        wx_ctrl: Optional[WechatHookApi] = kwargs.get("wx_ctrl")
        if not wx_ctrl:
            return
        await self.call_api(
            wx_ctrl.api, method=wx_ctrl.method.value, data=wx_ctrl.post_data
        )

    async def handle_event(self, event: Event) -> None:
        logger.debug(f"event is to me {event.is_tome()}")
        await handle_event(self, event)

    async def send_msg(self, msg, data):
        data["method"] = "POST"
        await self.call_api("text", data=data)
