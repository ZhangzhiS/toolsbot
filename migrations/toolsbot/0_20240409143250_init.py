from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "wechat_bot" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "delete_time" BIGINT NOT NULL,
    "token" VARCHAR(64) NOT NULL,
    "api_host" VARCHAR(64) NOT NULL,
    "wxid" VARCHAR(32) NOT NULL,
    "nickname" VARCHAR(32) NOT NULL,
    "status" BOOL NOT NULL  DEFAULT True
);
COMMENT ON COLUMN "wechat_bot"."token" IS '访问微信 http API 的 token';
COMMENT ON COLUMN "wechat_bot"."api_host" IS '微信httpAPI地址';
COMMENT ON COLUMN "wechat_bot"."wxid" IS '机器人微信的 wxid';
COMMENT ON COLUMN "wechat_bot"."nickname" IS '机器人微信的昵称';
COMMENT ON COLUMN "wechat_bot"."status" IS '机器人的状态';
COMMENT ON TABLE "wechat_bot" IS '微信机器人表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
