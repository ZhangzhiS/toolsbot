import os
import json
from typing import Any
from typing_extensions import override

from nonebot import get_plugin_config, logger
from nonebot.exception import WebSocketClosed
from nonebot.utils import DataclassEncoder, escape_tag
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    WebSocket,
    ForwardDriver,
    ReverseDriver,
    ASGIMixin,
    HTTPClientMixin,
    HTTPServerSetup,
    WebSocketServerSetup,
)

from nonebot.adapters import Adapter as BaseAdapter


from .bot import Bot
from .log import log
from .event import Event
from .config import Config
from .model import GetUserInfoResponse
from .message import Message, MessageSegment


class Adapter(BaseAdapter):

    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.default_wechat_url = "http://192.168.68.111:10010/"
        self.bot: Bot
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
        self.driver.on_startup(self.register_bot)

    def check_at_bot(self, msg_content: str) -> bool:
        return f"@{self.bot_config.nickname}" in msg_content

    async def __handle_http(self, request: Request) -> Response:
        if (data := request.content) is not None:
            data = json.loads(data)
        if not isinstance(data, dict):
            return Response(500, content="Received non-JSON data, cannot cast to dict")
        data["is_at_me"] = self.check_at_bot(data.get("content", ""))
        del data["xml"]
        if event := Event.json_to_event(data):
            await self.bot.handle_event(event)
        return Response(200)

    async def send_request(self, request: Request):
        if not isinstance(self.driver, HTTPClientMixin):
            raise RuntimeError(
                f"Current driver {self.config.driver} "
                "doesn't support http client requests!"
                f"{self.get_name()} Adapter needs a HTTPClient Driver to work."
            )
        return await self.driver.request(request)

    async def register_bot(self):
        api = "userinfo"
        url = os.path.join(self.default_wechat_url, api)
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
            log("DEBUG", str(userinfo_resp))
            bot_config = Config(
                wxid=userinfo_resp.data.wxid,
                url=self.default_wechat_url,
                nickname=userinfo_resp.data.name,
            )
            self.bot_config = bot_config
            self.bot = Bot(self, self_id=userinfo_resp.data.wxid, config=bot_config)
            self.bot_connect(self.bot)

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
        url = os.path.join(bot.wx_config.url, api)
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
