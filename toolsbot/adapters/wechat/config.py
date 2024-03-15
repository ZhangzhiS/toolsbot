from pydantic import Field, BaseModel


class Config(BaseModel):
    wxid: str
    url: str
    nickname: str

