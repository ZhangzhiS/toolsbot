import os
import nonebot

from toolsbot.adapters.wechat.adapter import Adapter as WechatAdapter

e_file = "/etc/project/toolsbot/.env"

if os.path.exists(".env"):
    e_file = ""

nonebot.init(_env_file=e_file)

driver = nonebot.get_driver()
driver.register_adapter(WechatAdapter)
nonebot.load_from_toml("pyproject.toml")
from services.db_context import disconnect, init  # noqa: E402

driver.on_startup(init)
driver.on_shutdown(disconnect)


if __name__ == "__main__":
    nonebot.run(port=8088)
