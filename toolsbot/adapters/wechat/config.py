from pydantic import Field, BaseModel


class Config(BaseModel):
    wxid: str
    callback_url: str
    nickname: str

