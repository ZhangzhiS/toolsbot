from services.db_context import ModelBase
from tortoise import fields


class WeChatBot(ModelBase):
    token = fields.CharField(64, description="访问微信 http API 的 token")
    api_host = fields.CharField(64, description="微信httpAPI地址")
    wxid = fields.CharField(32, description="机器人微信的 wxid")
    nickname = fields.CharField(32, description="机器人微信的昵称")
    status = fields.BooleanField(default=True, description="机器人的状态")

    class Meta:
        table = "wechat_bot"
        table_description = "微信机器人表"
