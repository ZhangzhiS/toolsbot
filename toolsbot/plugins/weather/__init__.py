from nonebot import on_command, on_keyword, require
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from arclet.alconna import Alconna, Args

from toolsbot.adapters.wechat.event import Event

require("nonebot_plugin_htmlrender")

from .config import DEBUG, QWEATHER_APIKEY, QWEATHER_APITYPE, Config  # noqa: E402
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


weather = on_keyword({"天气",}, block=True, priority=1)


cmd_parse = Alconna("天气", Args["city", str])
cmd_parse.shortcut(r"^(?P<city>.+)天气$", {"args": ["{city}"], "fuzzy": False})
cmd_parse.shortcut(r"^天气(?P<city>.+)$", {"args": ["{city}"], "fuzzy": False})


@weather.handle()
async def _(event: Event):
    if QWEATHER_APIKEY is None or QWEATHER_APITYPE is None:
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

    if True:
        debug_save_img(img)

    # await weather.send("")


def debug_save_img(img: bytes) -> None:
    from io import BytesIO

    from PIL import Image

    logger.debug("保存图片到 weather.png")
    a = Image.open(BytesIO(img))
    a.save("weather.png", format="PNG")
