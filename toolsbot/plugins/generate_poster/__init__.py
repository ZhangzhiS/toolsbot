from nonebot import logger, on_command
from nonebot.internal.adapter import Message
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

__plugin_meta__ = PluginMetadata(
    name="生成海报",
    description="通过图片生成带有二维码的海报",
    usage="没什么用",
    type="application",
    extra={},
)


gen_poster = on_command(
    ("help",),
    rule=to_me()
)


@gen_poster.handle()
async def handle_function(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("location", args)


@gen_poster.got("location", prompt="请输入地名")
async def got_location(location: str = ArgPlainText()):
    logger.info(f"""
    location: {location}
    """)
    await gen_poster.finish(f"今天{location}的天气是...")
