import json
from typing import Any
from typing_extensions import override

from nonebot import get_plugin_config, logger
from nonebot.exception import WebSocketClosed
from nonebot.utils import DataclassEncoder, escape_tag
from nonebot.drivers import (
    URL,
    ASGIMixin,
    Driver,
    HTTPClientMixin,
    Request,
    Response,
    WebSocket,
    ForwardDriver,
    ReverseDriver,
    HTTPServerSetup,
    WebSocketServerSetup,
)

from nonebot.adapters import Adapter as BaseAdapter

from .bot import Bot
from .event import Event
from .config import Config
from .model import CallBackPayload
from .message import Message, MessageSegment
from .exception import WechatHookException


class Adapter(BaseAdapter):

    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        if not isinstance(self.driver, HTTPClientMixin):
            raise RuntimeError(
                f"Current driver {self.config.driver} "
                "doesn't support http client requests!"
                f"{self.get_name()} Adapter needs a HTTPClient Driver to work."
            )
        if not isinstance(self.driver, ASGIMixin):
            raise RuntimeError(
                f"Current driver {self.config.driver} "
                "doesn't support reverse connections!"
                f"{self.get_name()} Adapter needs a ASGI Driver to work."
            )
        self.setup()


    def setup(self) -> None:
        setup = HTTPServerSetup(
            URL("/wechat/callback"),
            "POST",
            self.get_name(),
            self.__handle_http,
        )
        self.setup_http_server(setup)

    async def _register_bot(self, config: Config) -> None:
        pass

    async def check_register_robot(self, wxid: str, host: str) -> None:
        if self.bots.get(wxid):
            return
        return await self._register_bot(wxid, host)

    def _check_request(self, request: Request) -> Config:
        if request.method != "POST":
            raise WechatHookException("请求方式错误")
        url = URL(request.url)
        wxid = url.query.get("robot")
        host = url.query.get("host")
        if not wxid or not host:
            raise WechatHookException("请求缺少参数")
        config = dict(wxid=wxid, callback_url=str(url), nickname="")
        return Config.model_validate(config)

    def _json_to_event(self, bot: Bot, hook_msg: CallBackPayload) -> Event:
        if hook_msg.is_self:
            hook_msg.to_me = False
        elif not hook_msg.is_group and not hook_msg.is_self:
            hook_msg.to_me = True
        elif hook_msg.is_group and f"@{bot.config.nickname}" in hook_msg.content:
            hook_msg.to_me = True
            if not hook_msg.content:
                pass
            if f"@{bot.config.nickname}" in hook_msg.content:
                hook_msg.to_me = True
        return Event.json_to_event(hook_msg.model_dump())

    async def __handle_http(self, request: Request) -> Response:
        try:
            config = self._check_request(request)
        except WechatHookException as e:
            logger.error(e)
            return Response(400, content=str(e))
        # if event := Event.json_to_event(data):
        #     await self.bot.handle_event(event)
        if not self.bots.get(config.wxid):
            await self._register_bot(config)
        bot = self.bots.get(config.wxid)
        data = request.json
        logger.warning(request.content)
        msg = CallBackPayload.model_validate(data)
        logger.error(f"""
                     {data}
        """)
        return Response(200)

    @classmethod
    @override
    def get_name(cls) -> str:
        return "WeChat Rest"

    @override
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        pass
