from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "positionidmap" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "wxid" VARCHAR(64) NOT NULL,
    "position_id" INT NOT NULL,
    "withdrawal_amount" INT NOT NULL  DEFAULT 0,
    "withdrawal_count" INT NOT NULL  DEFAULT 0
);
COMMENT ON COLUMN "positionidmap"."wxid" IS '微信 id';
COMMENT ON COLUMN "positionidmap"."position_id" IS '推广位 id';
COMMENT ON COLUMN "positionidmap"."withdrawal_amount" IS '已提现金额';
COMMENT ON COLUMN "positionidmap"."withdrawal_count" IS '已提现次数';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "positionidmap";"""
