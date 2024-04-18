import datetime
from urllib.parse import urljoin

import asyncio_oss
from nonebot.rule import to_me
import oss2
from arclet.alconna import Alconna, Args
from nonebot import on_keyword, require
from nonebot.log import logger
from nonebot.plugin import PluginMetadata

from toolsbot.adapters.wechat.event import Event
from toolsbot.adapters.wechat.message import SendImageMessage

require("nonebot_plugin_htmlrender")

from .config import (  # noqa: E402
    DEBUG,
    IMAGE_DOMAIN,
    OSS2_ACCESS_KEY_ID,
    OSS2_ACCESS_KEY_SECRET,
    OSS2_BUCKET_NAME,
    OSS2_ENDPOINT,
    OSS2_PATH_PREFIX,
    QWEATHER_APIKEY,
    QWEATHER_APITYPE,
    Config,
)
from .render_pic import render  # noqa: E402
from .weather_data import CityNotFoundError, ConfigError, Weather  # noqa: E402

__plugin_meta__ = PluginMetadata(
    name="天气",
    description="和风天气图片显示插件",
    usage="天气地名 / 地名天气",
    type="application",
    config=Config,
)


if DEBUG:
    logger.debug("将会保存图片到 weather.png")

OSS_AUTH = oss2.Auth(OSS2_ACCESS_KEY_ID, OSS2_ACCESS_KEY_SECRET)


weather = on_keyword(
    {
        "天气",
    },
    block=True,
    priority=1,
    rule=to_me(),
)


cmd_parse = Alconna("天气", Args["city", str])
cmd_parse.shortcut(r"^(?P<city>.+)天气$", {"args": ["{city}"], "fuzzy": False})
cmd_parse.shortcut(r"^天气(?P<city>.+)$", {"args": ["{city}"], "fuzzy": False})


@weather.handle()
async def _(event: Event):
    if (
        QWEATHER_APIKEY is None
        or QWEATHER_APITYPE is None
        or OSS2_ACCESS_KEY_SECRET is None
        or OSS2_ACCESS_KEY_ID is None
    ):
        raise ConfigError("请设置 qweather_apikey 和 qweather_apitype")

    params = cmd_parse.parse(event.content)
    if not params.matched:
        return await weather.finish("请查看输入命令")

    city = params.main_args.get("city", "")
    w_data = Weather(city_name=city, api_key=QWEATHER_APIKEY, api_type=QWEATHER_APITYPE)

    try:
        await w_data.load_data()
    except CityNotFoundError:
        logger.warning(f"找不到城市: {city}")
        weather.block = False
        return await weather.finish(f"找不到城市: {city}")

    img = await render(w_data)

    if False:
        debug_save_img(img)

    img_path = await save_to_oss(w_data.city_id, img)
    await weather.finish(SendImageMessage(img_path))


async def save_to_oss(city_id, img: bytes) -> str:
    key_time = datetime.datetime.today().strftime("%Y-%m-%d")
    key = f"{OSS2_PATH_PREFIX}/{key_time}-{city_id}.png"
    logger.info(key)
    async with asyncio_oss.Bucket(OSS_AUTH, OSS2_ENDPOINT, OSS2_BUCKET_NAME) as bucket:
        if await bucket.object_exists(key):
            return urljoin(IMAGE_DOMAIN or "https://img.zzs7.top", key)
        await bucket.put_object(key, img)
    return urljoin(IMAGE_DOMAIN or "https://img.zzs7.top", key)


def debug_save_img(img: bytes) -> None:
    from io import BytesIO

    from PIL import Image

    logger.debug("保存图片到 weather.png")
    a = Image.open(BytesIO(img))
    a.save("weather.png", format="PNG")
