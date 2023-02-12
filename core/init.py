from loguru import logger
from core.manager.plugins import load_plugins


async def init():
    logger.info("初始化加载数据")
    await load_plugins()
