# import enum
# from typing import Optional
# from nonebot.drivers import Request
# from pydantic import BaseModel
#
# class METHOD(str, enum.Enum):
#     POST = "POST"
#     GET = "GET"
#
#
# class WechatHookApiBase(BaseModel):
#
#     api: str
#     method: METHOD
#     params: Optional[dict]
#     data: Optional[dict]
#
#     def to_request(self) -> Request:
#         req = Request(
#             data["method"],
#             url,
#             json=data.get("data"),
#         )
#         return req
