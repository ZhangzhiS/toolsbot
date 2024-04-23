from typing import List, Optional
from pydantic import BaseModel, Field


class CreateWeChatBot(BaseModel):
    wxid: str = Field(..., description="微信 id")
    callback_url: str = Field(..., description="回调 url")
    name: str = Field(..., description="昵称，便于区分机器人")
    token: Optional[str] = Field(None, description="token")
    remark: Optional[str] = Field(None, description="备注")


class DeleteWeChatBotParams(BaseModel):
    wxid: str = Field(..., description="微信 id")


class CreateWebHookParams(BaseModel):
    bot_id: str = Field(..., description="要使用的机器人的微信 id")
    receiver: str = Field(
        ..., description="接收者，私聊联系人的 wxid 或者群聊的 room_id"
    )
    receiver_name: str = Field(..., description="接收者的昵称")
    bot_type: str = Field("wechat", description="机器人的类型")
    remark: Optional[str] = Field(default="", description=" 备注")


class WebHookParams(BaseModel):
    tokens: List[str] = Field(..., description="token")
    msg: str = Field(..., description="推送的消息")
