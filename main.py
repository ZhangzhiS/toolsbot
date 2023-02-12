import nonebot
from nonebot.adapters.onebot.v11 import Adapter

from core.init import init


nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# 初始数据
driver.on_startup(init)

# 加载插件
# nonebot.load_plugins("plugins")
nonebot.load_plugin("plugins.dong")
nonebot.load_plugin("plugins.ding")

app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
