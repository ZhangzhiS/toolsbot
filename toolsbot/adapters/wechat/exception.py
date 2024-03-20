from nonebot.exception import AdapterException


class WcfAdapterException(AdapterException):
    def __init__(self):
        super().__init__("WeChat")


class WechatHookException(WcfAdapterException):

    def __init__(self, info: str):
        super().__init__()
        self.info = info

    def __repr__(self) -> str:
        return f"""
        Hook客户端请求异常：{self.info}
        """
