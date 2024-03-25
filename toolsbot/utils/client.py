#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum
from typing import Any, Dict, Optional 

import httpx


class METHOD(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BaseRequest:
    url: str
    method: METHOD
    response: Any
    params: Dict[str, Any] = {}
    json: Dict[Any, Any] = {}
    path_params: Optional[Dict[str, Any]] = None


class BaseClient:
    def __init__(self, host):
        self._host = host

    def prepare(self, request: BaseRequest) -> httpx.Request:
        if request.path_params:
            url = request.url.format(**request.path_params)
        else:
            url = request.url
        url = f"{self._host}{url}"
        req = httpx.Request(
            method=request.method.value,
            url=url,
            params=request.params,
            json=request.json,
        )
        return req

