import os
from typing import  TYPE_CHECKING, List, Union, Any
from typing_extensions import override
from nonebot import logger

from nonebot.adapters import Bot as BaseBot
from nonebot.message import handle_event

from .event import Event
from .message import Message, MessageSegment
from .config import Config

if TYPE_CHECKING:
    from .adapter import Adapter


class Bot(BaseBot):

    @override
    def __init__(self, adapter: "Adapter", self_id: str, config: Config, **kwargs: Any):
        super().__init__(adapter, self_id)
        self.wx_config: Config = config

    @override
    async def send(
        self,
        event: Event,
        message: Union[str, Message, MessageSegment],
        **kwargs,
    ) -> Any:
        api = event.api()
        method = event.method()
        data = event.reply_data(message)
        await self.call_api(api, method=method, data=data)

    async def handle_event(self, event: Event) -> None:
        logger.debug(f"event is to me {event.is_tome()}")
        await handle_event(self, event)
