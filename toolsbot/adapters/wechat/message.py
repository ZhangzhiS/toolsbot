from typing import Type, Union, Mapping, Iterable
from typing_extensions import override
from nonebot import logger

from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment

from toolsbot.adapters.wechat.model import TextMsgReply


class MessageSegment(BaseMessageSegment["Message"]):

    @classmethod
    @override
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


class DiscountSegment(MessageSegment):
    pass


class Message(BaseMessage[MessageSegment]):

    @classmethod
    @override
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @staticmethod
    @override
    def _construct(msg: str) -> Iterable[MessageSegment]:
        yield MessageSegment.text(msg)


