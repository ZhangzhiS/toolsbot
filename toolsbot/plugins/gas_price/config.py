from typing import Optional
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Plugin Config Here"""

    tanshu_api_key: Optional[str] = Field(default=None)
