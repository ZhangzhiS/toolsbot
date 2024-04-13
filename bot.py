import nonebot

from toolsbot.adapters.wechat.adapter import Adapter as WechatAdapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(WechatAdapter)
nonebot.load_from_toml("pyproject.toml")
from services.db_context import disconnect, init  # noqa: E402

driver.on_startup(init)
driver.on_shutdown(disconnect)


if __name__ == "__main__":
    nonebot.run()
