from typing import Optional
from pydantic import BaseModel


class CreateWeChatBot(BaseModel):
    wxid: str
    callback_url: str
    token: Optional[str] = None
    nickname: Optional[str] = None
    code: Optional[str] = None
