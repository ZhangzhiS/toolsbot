import asyncio
import os
import json
from typing import Any, cast
from typing_extensions import override
from nonebot import logger

from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    ASGIMixin,
    HTTPClientMixin,
    HTTPServerSetup,
)

from nonebot.adapters import Adapter as BaseAdapter


from .bot import Bot
from .event import Event
from .config import Config
from .exception import WechatHookException
from .model import GetUserInfoResponse
from toolsbot.utils.auth import parse_code


class Adapter(BaseAdapter):
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.default_wechat_url = "http://192.168.68.111:10010/"
        self.bot_config: Config
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
        # self.driver.on_startup(self._register_bot)

    def check_at_bot(self, bot, msg_content: str) -> bool:
        return f"@{bot.wx_config.nickname}" in msg_content

    async def _register_bot(self, config: Config) -> None:
        api = "userinfo"
        url = os.path.join(config.callback_url, api)
        req = Request(
            "get",
            url,
        )
        resp = await self.send_request(req)
        if resp.status_code != 200:
            return
        if (data := resp.content) is not None:
            data = json.loads(data)
            userinfo_resp = GetUserInfoResponse.model_validate(data)
            bot_config = Config(
                wxid=userinfo_resp.data.wxid,
                callback_url=self.default_wechat_url,
                nickname=userinfo_resp.data.name,
            )
            self.bot_config = bot_config
            bot = Bot(self, self_id=userinfo_resp.data.wxid, config=bot_config)
            self.bot_connect(bot)

    def _check_request(self, request: Request) -> Config:
        if request.method != "POST":
            raise WechatHookException("请求方式错误")
        url = URL(request.url)
        code = url.query.get("code")
        wxid, host = parse_code(code)
        if not wxid or not host:
            raise WechatHookException("请求缺少参数")
        config = dict(wxid=wxid, callback_url=host, nickname="")
        logger.warning(config)
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
        data["is_at_me"] = self.check_at_bot(bot, data.get("content", ""))
        del data["xml"]
        if event := Event.json_to_event(data):
            asyncio.create_task(cast(Bot, bot).handle_event(event))
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
