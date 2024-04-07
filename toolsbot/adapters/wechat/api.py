import enum
from typing import Any, Optional
from pydantic import BaseModel


class METHOD(str, enum.Enum):
    POST = "POST"
    GET = "GET"


class WechatHookApi(BaseModel):

    api: str = ""
    method: METHOD = METHOD.GET

    def validate(self) -> bool:
        return True

class SendTextMessageAPI(WechatHookApi):
    api: Optional[str] = "text"
    method: Optional[METHOD] = METHOD.POST

class TextMessageParams(BaseModel):
    at: str
    receiver: str
    msg: str
