from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
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
COMMENT ON TABLE "webhook_auth" IS 'webhook 授权表';
CREATE TABLE IF NOT EXISTS "wechat_bot" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "user_id" VARCHAR(64),
    "token" VARCHAR(64),
    "callback_url" VARCHAR(64) NOT NULL,
    "wxid" VARCHAR(32) NOT NULL UNIQUE,
    "nickname" VARCHAR(32),
    "status" BOOL NOT NULL  DEFAULT True,
    "code" VARCHAR(255)
);
COMMENT ON COLUMN "wechat_bot"."user_id" IS '访问微信 http API 的 token';
COMMENT ON COLUMN "wechat_bot"."token" IS '访问微信 http API 的 token';
COMMENT ON COLUMN "wechat_bot"."callback_url" IS '微信httpAPI地址';
COMMENT ON COLUMN "wechat_bot"."wxid" IS '机器人微信的 wxid';
COMMENT ON COLUMN "wechat_bot"."nickname" IS '机器人微信的昵称';
COMMENT ON COLUMN "wechat_bot"."status" IS '机器人的状态';
COMMENT ON COLUMN "wechat_bot"."code" IS '请求平台code';
COMMENT ON TABLE "wechat_bot" IS '微信机器人表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
