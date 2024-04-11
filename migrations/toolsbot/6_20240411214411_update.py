from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "webhook_auth" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" VARCHAR(64),
    "token" VARCHAR(64),
    "bot_type" VARCHAR(6) NOT NULL
);
COMMENT ON COLUMN "webhook_auth"."user_id" IS '用户 id';
COMMENT ON COLUMN "webhook_auth"."token" IS '推送服务需要的 token';
COMMENT ON COLUMN "webhook_auth"."bot_type" IS '机器人类型';
COMMENT ON TABLE "webhook_auth" IS 'webhook 授权表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "webhook_auth";"""
