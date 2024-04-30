from decimal import Decimal
from tortoise import fields
from services.db_context import ModelBase, TimestampMixin


class JdRebate(ModelBase):
    order_id = fields.CharField(64, description="订单号")
    order_time = fields.CharField(64, description="订单时间")
    modify_time = fields.CharField(64, description="修改时间")
    finish_time = fields.CharField(64, description="完成时间")
    price = fields.DecimalField(
        default=Decimal("0"), description="商品价格", max_digits=10, decimal_places=2
    )
    sub_union_id = fields.CharField(64, description="子推广 id，保存 wxid")
    position_id = fields.CharField(64, description="推广位 id，保存 wxid")
    sku_name = fields.CharField(255, description="商品名称")
    balance_ext = fields.CharField(64, description="佣金扩展信息")
    estimate_cos_price = fields.DecimalField(
        default=Decimal("0"),
        description="预估计算佣金的金额",
        max_digits=10,
        decimal_places=2,
    )
    estimate_fee = fields.DecimalField(
        default=Decimal("0"),
        description="预估佣金金额",
        max_digits=10,
        decimal_places=2,
    )
    actual_fee = fields.DecimalField(
        default=Decimal("0"),
        description="实际佣金金额",
        max_digits=10,
        decimal_places=2,
    )
    actual_cos_price = fields.DecimalField(
        default=Decimal("0"),
        description="实际计算佣金的金额",
        max_digits=10,
        decimal_places=2,
    )
    take_a_percentage = fields.CharField(
        3, default="15", description="机器人抽成佣金比例"
    )
    take_to_wxid = fields.IntField(default=0, description="实际分给wx 用户的金额")
    data = fields.JSONField(description="原始数据", defaule={})
