from typing import Dict

from nonebot import logger
from tortoise import fields

from services.db_context import ModelBase, TimestampMixin
from toolsbot.plugins.webapi.api import params


class WeChatBot(ModelBase, TimestampMixin):
    user_id = fields.CharField(64, null=True, description="访问微信 http API 的 token")
    token = fields.CharField(64, null=True, description="访问微信 http API 的 token")
    callback_url = fields.CharField(64, description="微信httpAPI地址")
    wxid = fields.CharField(32, description="机器人微信的 wxid", unique=True)
    nickname = fields.CharField(32, null=True, description="机器人微信的昵称")
    status = fields.BooleanField(default=True, description="机器人的状态")
    code = fields.CharField(255, null=True, description="请求平台code")

    class Meta:
        table = "wechat_bot"
        table_description = "微信机器人表"

    @classmethod
    async def create_or_update_bot(cls, info: params.CreateWeChatBot):
        bot = await cls.get_or_none(wxid=info.wxid)
        if bot:
            return await bot.update_from_dict(info.model_dump())
        return await cls.create(**info.model_dump())

    @classmethod
    async def get_bots(cls):
        bots = await cls.all().values("wxid", "nickname", "callback_url", "code")
        return bots
