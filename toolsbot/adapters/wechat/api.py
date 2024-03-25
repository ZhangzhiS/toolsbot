import enum
from typing import Any, Optional
from pydantic import BaseModel


class METHOD(str, enum.Enum):
    POST = "POST"
    GET = "GET"


class WechatHookApi(BaseModel):

    api: str = ""
    method: METHOD = METHOD.GET
    params: Optional[dict] = {}
    post_data: Optional[dict] = {}


class SendTextMessage(WechatHookApi):
    api: str = "text"
    method: METHOD = METHOD.POST

