from enum import Enum
from tortoise import fields

from services.db_context import ModelBase, TimestampMixin


class BotTypeEnum(Enum):
    WECHAT = "wechat"


class WebhookAuth(ModelBase, TimestampMixin):
    user_id = fields.CharField(64, null=True, description="用户 id")
    token = fields.CharField(64, null=True, description="推送服务需要的 token")
    bot_type = fields.CharEnumField(BotTypeEnum, null=False, description="机器人类型")

    class Meta:
        table = "webhook_auth"
        table_description = "webhook 授权表"


class WebhookHistory:
    pass
