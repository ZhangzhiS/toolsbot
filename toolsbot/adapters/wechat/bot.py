from typing import TYPE_CHECKING, Any, Optional, Union

from nonebot import logger
from nonebot.adapters import Bot as BaseBot
from nonebot.message import handle_event
from typing_extensions import override

from toolsbot.adapters.wechat.api import WechatHookApi
from toolsbot.adapters.wechat.exception import WechatHookException

from .config import Config
from .event import Event, GroupMessageEvent, PrivateMessageEvent
from .message import Message, MessageSegment, SendTextMessage

if TYPE_CHECKING:
    from .adapter import Adapter


def pre_build_msg(event: Event, msg: Union[str, "Message", "MessageSegment"]) -> Message:
    if isinstance(event, GroupMessageEvent):
        at = MessageSegment.at(event.sender)
    else:
        at = MessageSegment.at()
    if isinstance(msg, str):
        return SendTextMessage(msg) + at
    elif isinstance(msg, MessageSegment):
        if msg.is_text:
            return SendTextMessage(msg) + at
    elif isinstance(msg, Message):
        return msg
    raise WechatHookException("message 类型错误")

    
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
        receiver = kwargs.get("receiver")
        if not receiver:
            if isinstance(event, GroupMessageEvent):
                receiver = event.roomid
            else:
                receiver = event.sender
        msg: Message = pre_build_msg(event, message)
        if not msg.validate():
            return
        logger.debug(msg.serialize(receiver))
        await self.call_api(
            msg.req.api, method=msg.req.method.value, data=msg.serialize(receiver)
        )

    async def handle_event(self, event: Event) -> None:
        logger.debug(f"event is to me {event.is_tome()}")
        await handle_event(self, event)

    async def send_msg(self, msg, data):
        data["method"] = "POST"
        await self.call_api("text", data=data)
