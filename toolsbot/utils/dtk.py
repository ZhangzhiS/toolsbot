#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import hashlib
import operator
import os
from typing import Tuple

import httpx
from nonebot import get_plugin_config

# import aiohttp

from .client import BaseClient, BaseRequest, METHOD


from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""

    dtk_jd_unionid: int
    dtk_appkey: str
    dtk_secret: str
    dtk_host: str


settings = get_plugin_config(Config)


class GetJdUrl(BaseRequest):
    url = "api/dels/jd/kit/promotion-union-convert"
    method = METHOD.GET

    def __init__(self, material_id: str) -> None:
        super().__init__()
        self.params = {"materialId": material_id, "unionId": settings.dtk_jd_unionid}


class GetJdUrlContent(BaseRequest):
    url = "api/dels/jd/kit/content/promotion-union-convert"
    method = METHOD.GET

    def __init__(self, content: str) -> None:
        super().__init__()
        self.params = {"unionId": settings.dtk_jd_unionid, "content": content}


class AsyncClient(BaseClient):

    def __init__(self, version="v1.0.0"):
        self.appkey = settings.dtk_appkey
        self.app_secret = settings.dtk_secret
        self.version = version
        self._host = settings.dtk_host
        self._client = httpx.AsyncClient()

    @staticmethod
    def md5(arg):
        md5 = hashlib.md5()
        loc_bytes_utf8 = arg.encode(encoding="utf-8")
        md5.update(loc_bytes_utf8)
        return md5.hexdigest()

    """#key 加密算法 
    1：对传入的产生 按照key 进行排序
    2：将排序后的数据 将各数据字段 用字符串 ‘&’连接起来
    如：data={appkey:123,pageId:1} 处理后 appkey=123&pageId=1
    3:在处理后的数据字符串后追加 appSecret  如 appSecret=helloworld 则 最终 加密字符串为appkey=123&pageId=1&key=hellworld
    4：采用MD5加密算法对 处理后的字符串进行加密
    """

    def md5_sign(self, args):
        copy_args = copy.deepcopy(args)
        # 对传入的参数 按照key 排序
        sorted_args = sorted(copy_args.items(), key=operator.itemgetter(0))
        tmp = []
        for i in sorted_args:
            tmp.append("{}={}".format(list(i)[0], list(i)[1]))
        sign = self.md5("&".join(tmp) + "&" + "key={}".format(self.app_secret)).upper()
        copy_args["sign"] = sign
        return copy_args

    def prepare(self, request: BaseRequest) -> httpx.Request:
        if request.path_params:
            url = request.url.format(**request.path_params)
        else:
            url = request.url
        url = os.path.join(self._host, url)
        if request.method == METHOD.GET:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
                "content-length": "0",
                "Client-Sdk-Type": "python",
            }
            request.params["appKey"] = self.appkey
            request.params["version"] = self.version
            request.params = self.md5_sign(request.params)
            req = httpx.Request(
                method=request.method.value,
                url=url,
                params=request.params,
                # json=request.json,
                headers=headers,
            )
        else:
            request.json["appKey"] = self.appkey
            request.json = self.md5_sign(request.json)
            req = httpx.Request(
                method=request.method.value,
                url=url,
                json=request.json,
            )

        return req

    async def request(self, req: BaseRequest) -> Tuple[bool, dict]:
        prepared_req = self.prepare(req)
        resp = await self._client.send(prepared_req)
        print(resp.json())
        if resp.status_code != 200:
            return False, {"msg": resp.status_code}
        resp_data = resp.json()
        if resp_data["code"] == 1:
            return False, {"msg": resp_data.get("msg")}
        elif resp_data["code"] == -1:
            return False, {"msg": "服务器错误"}
        data = resp_data.get("data")
        return True, {"data": data}

    async def get_jd_url(self, url) -> str:
        status, resp = await self.request(GetJdUrl(url))
        if status:
            n = resp.get("data", {}).get("shortUrl", "")
            if not n:
                return url
            else:
                return n
        return url

    async def get_jd_url_content(self, content) -> str:
        status, resp = await self.request(GetJdUrlContent(content))
        if status:
            n = resp.get("data", {}).get("content", "")
            if n:
                return n
        return content


dtk_cli = AsyncClient()
