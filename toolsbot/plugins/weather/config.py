from typing import Optional

from nonebot import get_plugin_config
from pydantic import BaseModel, Field

from .model import HourlyType


class Config(BaseModel):
    qweather_apikey: Optional[str] = Field(default=None)
    qweather_apitype: Optional[int] = Field(default=None)
    qweather_hourlytype: Optional[HourlyType] = Field(default=HourlyType.current_12h)
    qweather_forecase_days: Optional[int] = Field(default=3)
    oss2_endpoint: Optional[str] = Field(default="oss-cn-beijing.aliyuncs.com")
    oss2_access_key_id: Optional[str] = Field(default=None)
    oss2_access_key_secret: Optional[str] = Field(default=None)
    image_domain: Optional[str] = Field(default="https://img.zzs7.top")
    debug: Optional[bool] = Field(default=False)


plugin_config: Config = get_plugin_config(Config)
QWEATHER_APIKEY = plugin_config.qweather_apikey
QWEATHER_APITYPE = plugin_config.qweather_apitype
QWEATHER_HOURLYTYPE = plugin_config.qweather_hourlytype
QWEATHER_FORECASE_DAYS = plugin_config.qweather_forecase_days
OSS2_ENDPOINT = plugin_config.oss2_endpoint
OSS2_ACCESS_KEY_ID = plugin_config.oss2_access_key_id
OSS2_ACCESS_KEY_SECRET = plugin_config.oss2_access_key_secret
OSS2_BUCKET_NAME = "make-money"
OSS2_PATH_PREFIX = "weather"
IMAGE_DOMAIN = plugin_config.image_domain
DEBUG = plugin_config.debug
