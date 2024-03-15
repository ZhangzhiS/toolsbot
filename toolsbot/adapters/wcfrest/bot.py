from typing import Union, Any, TYPE_CHECKING
from typing_extensions import override

from nonebot.adapters import Bot as BaseBot
from nonebot.message import handle_event

from .event import Event
from .config import Config
from .message import Message, MessageSegment

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
        await handle_event(self, event)
