from nonebot import on_command
# from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.adapters.onebot.v11 import MessageEvent, Message
from nonebot.params import CommandArg
# from services.log import logger
from nonebot.log import logger


# 插件的可读名称
__readable_name__ = "叮咚机器人"

# 插件描述
__plugin_des__ = "发dong回复ding"

# 插件帮助文本
__plugin_usage__ = """
usage：
    消息处理插件示例！
    收到：dong
    回复：ding
"""

# 插件版本
__plugin_version__ = 0.1

# 插件作者
__plugin_author__ = "ZhangS"

# 插件设置
# status 插件是否启用
__plugin_settings__ = {
    "status": True,
}

# 插件配置
# 如下示例
# """
# __plugin_configs__ = {
#     "key": {"value": 1, "help": "接口appkey"}
# }
# """
__plugin_configs__ = {
}


dong = on_command("dong", priority=5, block=True)


@dong.handle()
async def _dong(event: MessageEvent, arg: Message = CommandArg()):
    """叮咚测试"""
    msg = arg.extract_plain_text().strip().split()
    user_name = event.sender.card or event.sender.nickname
    if not msg:
        await dong.send(f"ding hello {user_name}", at_sender=True)
    logger.info(f"USERNAME: {user_name}")
