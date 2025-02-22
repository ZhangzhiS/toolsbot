import asyncio
import json
import os
from typing import Any, cast
from urllib.parse import urljoin

from nonebot import logger
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.drivers import (
    URL,
    ASGIMixin,
    Driver,
    HTTPClientMixin,
    HTTPServerSetup,
    Request,
    Response,
)
from typing_extensions import override

from toolsbot.utils.auth import decode_info

from .bot import Bot
from .config import Config
from .event import Event
from .exception import WechatHookException
from .model import GetUserInfoResponse


class Adapter(BaseAdapter):
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.env = self.driver.config.environment
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
            URL("/api/wechat/callback"),
            "POST",
            self.get_name(),
            self.__handle_http,
        )
        self.setup_http_server(setup)

    def check_at_bot(self, bot, data: dict) -> bool:
        at_me = f"@{bot.wx_config.name}" in data.get("content", "")
        if at_me:
            data["content"] = data["content"].replace(f"@{bot.wx_config.name}", "")
        return at_me

    async def _register_bot(self, config: Config) -> None:
        bot = Bot(self, self_id=config.wxid, config=config)
        self.bot_connect(bot)

    def _check_request(self, request: Request) -> Config:
        if request.method != "POST":
            raise WechatHookException("请求方式错误")
        code = request.headers.get("code", "")
        if not code:
            raise WechatHookException("请求缺少参数")
        info = decode_info(code)
        config = dict(
            wxid=info.get("wxid"),
            callback_url=info.get("callback_url"),
            name=info.get("name"),
        )
        if self.env == "dev":
            config["callback_url"] = "http://192.168.68.111:10010"
        return Config.model_validate(config)

    async def __handle_http(self, request: Request) -> Response:
        try:
            config = self._check_request(request)
        except WechatHookException as e:
            logger.error(e)
            return Response(400, content=str(e))
        if (data := request.content) is not None:
            data = json.loads(data)
        if not isinstance(data, dict):
            return Response(500, content="Received non-JSON data, cannot cast to dict")
        if not self.bots.get(config.wxid):
            await self._register_bot(config)
        bot = self.bots.get(config.wxid)
        data["is_at_me"] = self.check_at_bot(bot, data)
        del data["xml"]
        try:
            if event := Event.json_to_event(data):
                asyncio.create_task(cast(Bot, bot).handle_event(event))
        except ValueError:
            pass
        return Response(200)

    async def send_request(self, request: Request):
        if not isinstance(self.driver, HTTPClientMixin):
            raise RuntimeError(
                f"Current driver {self.config.driver} "
                "doesn't support http client requests!"
                f"{self.get_name()} Adapter needs a HTTPClient Driver to work."
            )
        return await self.driver.request(request)

    @classmethod
    @override
    def get_name(cls) -> str:
        return "WeChat"

    @override
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        if not isinstance(self.driver, HTTPClientMixin):
            raise RuntimeError(
                f"Current driver {self.config.driver} "
                "doesn't support http client requests!"
                f"{self.get_name()} Adapter needs a HTTPClient Driver to work."
            )
        url = os.path.join(bot.wx_config.callback_url, api)
        logger.info(f"Calling {url} with {data}")
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
