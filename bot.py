import nonebot
from toolsbot.adapters.wechat.adapter import Adapter as WechatAdapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(WechatAdapter)

nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()
