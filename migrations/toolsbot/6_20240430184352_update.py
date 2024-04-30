from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "jdrebate" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "order_id" VARCHAR(64) NOT NULL,
    "order_time" VARCHAR(64) NOT NULL,
    "modify_time" VARCHAR(64) NOT NULL,
    "finish_time" VARCHAR(64) NOT NULL,
    "price" DECIMAL(10,2) NOT NULL  DEFAULT 0,
    "sub_union_id" VARCHAR(64) NOT NULL,
    "position_id" VARCHAR(64) NOT NULL,
    "sku_name" VARCHAR(64) NOT NULL,
    "balance_ext" VARCHAR(64) NOT NULL,
    "estimate_cos_price" DECIMAL(10,2) NOT NULL  DEFAULT 0,
    "estimate_fee" DECIMAL(10,2) NOT NULL  DEFAULT 0,
    "actual_fee" DECIMAL(10,2) NOT NULL  DEFAULT 0,
    "actual_cos_price" DECIMAL(10,2) NOT NULL  DEFAULT 0,
    "take_a_percentage" VARCHAR(3) NOT NULL  DEFAULT '15',
    "take_to_wxid" INT NOT NULL  DEFAULT 0,
    "data" JSONB NOT NULL
);
COMMENT ON COLUMN "jdrebate"."order_id" IS '订单号';
COMMENT ON COLUMN "jdrebate"."order_time" IS '订单时间';
COMMENT ON COLUMN "jdrebate"."modify_time" IS '修改时间';
COMMENT ON COLUMN "jdrebate"."finish_time" IS '完成时间';
COMMENT ON COLUMN "jdrebate"."price" IS '商品价格';
COMMENT ON COLUMN "jdrebate"."sub_union_id" IS '子推广 id，保存 wxid';
COMMENT ON COLUMN "jdrebate"."position_id" IS '推广位 id，保存 wxid';
COMMENT ON COLUMN "jdrebate"."sku_name" IS '商品名称';
COMMENT ON COLUMN "jdrebate"."balance_ext" IS '佣金扩展信息';
COMMENT ON COLUMN "jdrebate"."estimate_cos_price" IS '预估计算佣金的金额';
COMMENT ON COLUMN "jdrebate"."estimate_fee" IS '预估佣金金额';
COMMENT ON COLUMN "jdrebate"."actual_fee" IS '实际佣金金额';
COMMENT ON COLUMN "jdrebate"."actual_cos_price" IS '实际计算佣金的金额';
COMMENT ON COLUMN "jdrebate"."take_a_percentage" IS '机器人抽成佣金比例';
COMMENT ON COLUMN "jdrebate"."take_to_wxid" IS '实际分给wx 用户的金额';
COMMENT ON COLUMN "jdrebate"."data" IS '原始数据';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "jdrebate";"""
