import asyncio
import json
import os
from typing import Any, cast
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
from .model import CallBackPayload, LoginWxUserInfo, LoginWxUserResponse
from .message import Message, MessageSegment
from .exception import WechatHookException


class Adapter(BaseAdapter):

    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.setup()


    def setup(self) -> None:
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
        setup = HTTPServerSetup(
            URL("/wechat/callback"),
            "POST",
            self.get_name(),
            self.__handle_http,
        )
        self.setup_http_server(setup)

    async def send_request(self, request: Request):
        if not isinstance(self.driver, HTTPClientMixin):
            raise RuntimeError(
                f"Current driver {self.config.driver} "
                "doesn't support http client requests!"
                f"{self.get_name()} Adapter needs a HTTPClient Driver to work."
            )
        return await self.driver.request(request)

    async def _register_bot(self, config: Config) -> None:
        api = "wcf/self_info"
        url = os.path.join(config.callback_url, api)
        logger.warning(url)
        req = Request(
            "post",
            url,
        )
        resp = await self.send_request(req)
        logger.warning(f"Resp{resp.content}")
        if resp.status_code != 200:
            return
        if (data := resp.content) is not None:
            data = json.loads(data)
            userinfo_resp = LoginWxUserResponse.model_validate(data)
            # log("DEBUG", str(userinfo_resp))
            config.nickname = userinfo_resp.Payload.name
            # self.bot_config = bot_config
            self.bot = Bot(self, self_id=config.wxid, config=config)
            self.bot_connect(self.bot)

    def _check_request(self, request: Request) -> Config:
        if request.method != "POST":
            raise WechatHookException("请求方式错误")
        url = URL(request.url)
        wxid = url.query.get("robot")
        host = url.query.get("host")
        if not wxid or not host:
            raise WechatHookException("请求缺少参数")
        config = dict(wxid=wxid, callback_url=host, nickname="")
        return Config.model_validate(config)

    def _parse_to_event(self, bot: Bot, hook_msg: CallBackPayload) -> Event:
        if hook_msg.is_self:
            hook_msg.to_me = False
            hook_msg.is_group = False
        elif not hook_msg.is_group and not hook_msg.is_self:
            hook_msg.is_self = False
            hook_msg.is_group = False
            hook_msg.to_me = True
        elif hook_msg.is_group and f"@{bot.config.nickname}" in hook_msg.content:
            hook_msg.to_me = True
        return Event.json_to_event(hook_msg.model_dump())

    async def __handle_http(self, request: Request) -> Response:
        try:
            config = self._check_request(request)
        except WechatHookException as e:
            logger.error(e)
            return Response(400, content=str(e))
        if not self.bots.get(config.wxid):
            await self._register_bot(config)
        bot = self.bots.get(config.wxid)
        if bot:
            data = request.json
            logger.warning(bot)
            msg = CallBackPayload.model_validate(data)
            event = self._parse_to_event(bot, msg)
            asyncio.create_task(cast(Bot, bot).handle_event(event))
        return Response(200)

    @classmethod
    @override
    def get_name(cls) -> str:
        return "WeChat Rest"

    @override
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        if not isinstance(self.driver, HTTPClientMixin):
            raise RuntimeError(
                f"Current driver {self.config.driver} "
                "doesn't support http client requests!"
                f"{self.get_name()} Adapter needs a HTTPClient Driver to work."
            )
        url = os.path.join(bot.wx_config.callback_url, api)
        req = Request(
            data["method"],
            url,
            json=data.get("data"),
        )
        try:
            response = await self.driver.request(req)
            if 200 <= response.status_code < 300:
                if not response.content:
                    raise ValueError("Empty response")
        except Exception as e:
            raise Exception("HTTP request failed") from e
