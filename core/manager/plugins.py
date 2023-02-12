from typing import Any
from types import ModuleType

# from path import Path

from core.db.mongodb_conn import db

plugins_attrs = [
    "__plugin_name__",
    "__plugin_des__",
    "__plugin_usage__",
    "__plugin_version__",
    "__plugin_author__",
    "__plugin_settings__",
    "__plugin_config__",
]


def get_attr(module: ModuleType, name: str, default: Any = None) -> Any:
    """
    说明:
        获取属性
    参数:
        :param module: module
        :param name: name
        :param default: default
    """
    return getattr(module, name) if hasattr(module, name) else default


async def load_plugins():
    """加载插件的信息"""
    plugins_data = db.test_collection.find()
    async for plugin in plugins_data:
        print(plugin)
