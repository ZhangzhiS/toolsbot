import nonebot
from loguru import logger
from core.manager.plugins import load_plugins


async def init():
    config = nonebot.get_driver().config
    logger.info(config.mongodb_host)
    await load_plugins()
