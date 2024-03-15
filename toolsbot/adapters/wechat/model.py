from enum import Enum
from typing import Any
from nonebot.compat import ConfigDict
from pydantic import BaseModel


class MSG_TYPE(Enum):
    UNKNOWN = 0
    TEXT_MSG = 1
    IMAGE_MSG = 3
    VOICE_MSG = 34
    OTHER_MSG = 51
    INVITE_INTO_GROUP = 10000


class WechatUserInfo(BaseModel):
    wxid: str
    name: str
    mobile: str
    home: str


class MessagePayload(BaseModel):
    is_self: bool
    is_group: bool
    id: int
    msg_type: MSG_TYPE
    ts: int
    roomid: str
    content: str
    sender: str
    sign: str
    thumb: str
    extra: str
    xml: str

    def __init__(self, /, **data: Any) -> None:
        if "type" in data:
            data["msg_type"] = MSG_TYPE(data["type"])
        super().__init__(**data)



class WeChatHttpApiResponse(BaseModel):
    status: int
    error: str | None
    data: Any


class GetUserInfoResponse(WeChatHttpApiResponse):
    data: WechatUserInfo
