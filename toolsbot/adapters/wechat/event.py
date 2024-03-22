from nonebot import logger
from typing_extensions import override

from nonebot.adapters import Event as BaseEvent

from .message import Message
from .model import MSG_TYPE


class Event(BaseEvent):
    is_self: bool
    is_group: bool
    sender: str
    content: str
    type: int
    is_at_me: bool
    roomid: str

    @classmethod
    def json_to_event(cls, data: dict) -> "Event":
        event_map = {
            MSG_TYPE.TEXT_MSG.value: MessageEvent,
            MSG_TYPE.NOTICE_MSG.value: NoticeEvent,
        }
        _type = data.get("type", 0)
        logger.error(data)
        if not _type:
            raise ValueError("CallBack type NOT FOUND!!")
        if _type not in event_map:
            raise ValueError("CallBack type ERROR!!")
        if _type == 1:
            if data.get("is_group"):
                return GroupMessageEvent.model_validate(data)
            else:
                return PrivateMessageEvent.model_validate(data)
        return event_map[_type].model_validate(data)

    @override
    def get_type(self) -> str:
        return "message"

    @override
    def get_event_name(self) -> str:
        return MSG_TYPE(self.type).name

    @override
    def get_event_description(self) -> str:
        return f"{self.__class__} {self.content}"

    @override
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @override
    def get_user_id(self) -> str:
        raise ValueError("Event has no user_id!")

    @override
    def get_session_id(self) -> str:
        return self.sender

    @override
    def is_tome(self) -> bool:
        if self.is_group and self.is_at_me is False:
            return True
        return True

    def api(self) -> str:
        raise ValueError("Event has no api!")

    def method(self) -> str:
        raise ValueError("Event has no method!")

    def reply_data(self, message: str) -> dict:
        raise ValueError("Event has no reply_data!")


class MessageEvent(Event):
    @override
    def is_tome(self) -> bool:
        return True

    @override
    def get_type(self) -> str:
        return "message"

    def get_message(self) -> Message:
        msg = Message(self.content)
        # msg_seq = MessageSegment("text", {"data": self.content})
        # msg.append(msg_seq)
        return msg

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


class GroupMessageEvent(MessageEvent):
    @override
    def is_tome(self) -> bool:
        return self.is_at_me


class PrivateMessageEvent(MessageEvent):
    @override
    def is_tome(self) -> bool:
        return True


class NoticeEvent(Event):

    def get_type(self) -> str:
        return "notice"
