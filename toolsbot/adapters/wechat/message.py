from typing import Iterable, Type

from nonebot.adapters import (
    Message as BaseMessage,
)
from nonebot.adapters import (
    MessageSegment as BaseMessageSegment,
)
from typing_extensions import override


class MessageSegment(BaseMessageSegment["Message"]):

    @classmethod
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @override
    def __str__(self) -> str:
        return self.data.get("text", "")

    @override
    def is_text(self) -> bool:
        return True

    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"text": text})

    @staticmethod
    def text_reply(data: dict) -> "MessageSegment":
        return MessageSegment("text", data)


class Message(BaseMessage[MessageSegment]):
    @classmethod
    @override
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @staticmethod
    @override
    def _construct(msg: str) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)
