from enum import Enum
from typing_extensions import override

from pydantic import BaseModel
from nonebot.adapters import Event as BaseEvent
from nonebot.compat import model_dump

from .message import Message


class EventType(Enum):
    UNKNOWN = -1
    PYQ = 0
    TEXT_MESSAGE = 1


class Event(BaseEvent):

    is_self: bool
    is_group: bool
    sender: str
    content: str
    type_: int
    is_at_me: bool
    roomid: str
    to_me: bool

    @classmethod
    def json_to_event(cls, data: dict) -> "Event":
        event_map = {
            1: MessageEvent,
        }
        _type = data.get("type", 0)
        if _type is None:
            raise ValueError("CallBack type Error!!")
        if _type not in event_map:
            raise ValueError("CallBack type ERROR!!")
        return event_map[_type].model_validate(data)

    @override
    def get_type(self) -> str:
        return str(self.type_)

    @override
    def get_event_name(self) -> str:
        return EventType(self.type_).name

    @override
    def get_event_description(self) -> str:
        return self.content

    @override
    def get_message(self) -> Message:
        raise ValueError("Event has not message")

    @override
    def get_plaintext(self) -> str:
        raise ValueError("Event has no plaintext!")

    @override
    def get_user_id(self) -> str:
        raise ValueError("Event has no user_id!")

    @override
    def get_session_id(self) -> str:
        raise ValueError("Event has no session_id!")

    @override
    def is_tome(self) -> bool:
        return self.to_me

    def api(self) -> str:
        raise ValueError("Event has no api!")

    def method(self) -> str:
        raise ValueError("Event has no method!")

    def reply_data(self, message: str) -> dict:
        raise ValueError("Event has no reply_data!")


class MessageEvent(Event):

    @override
    def get_type(self) -> str:
        return "message"

    def get_message(self) -> Message:
        return Message("self.content")

    def get_plaintext(self) -> str:
        return self.content

    def api(self) -> str:
        return "text"
    
    def method(self) -> str:
        return "post"
    
    def reply_data(self, message: str) -> dict:
        receiver = self.sender
        if self.is_group:
            receiver = self.roomid
        return dict(receiver=receiver, msg=message, aters="")

