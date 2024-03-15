from typing import Any, Optional
from pydantic import BaseModel


class CallBackPayload(BaseModel):
    is_self: Optional[bool] = None
    is_group: Optional[bool] = None
    id: int
    type: int
    ts: int
    roomid: Optional[str] = None
    content: Any
    sender: str
    sign: Optional[str] = None
    thumb: Optional[str] = None
    extra: Optional[str] = None
    xml: Any
    to_me: Optional[bool] = None


