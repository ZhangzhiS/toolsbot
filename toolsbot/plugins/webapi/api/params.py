from typing import Optional
from pydantic import BaseModel


class CreateWeChatBot(BaseModel):
    wxid: str
    callback_url: str
    token: Optional[str] = None
