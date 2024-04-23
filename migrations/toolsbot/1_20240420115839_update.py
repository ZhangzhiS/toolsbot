from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "wechat_bot_contact" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "bot_id" VARCHAR(32) NOT NULL,
    "wxid" VARCHAR(32) NOT NULL,
    "name" VARCHAR(32),
    "remark" VARCHAR(32)
);
COMMENT ON COLUMN "wechat_bot_contact"."bot_id" IS '机器人微信的 wxid';
COMMENT ON COLUMN "wechat_bot_contact"."wxid" IS '联系人 wxid';
COMMENT ON COLUMN "wechat_bot_contact"."name" IS '联系人昵称';
COMMENT ON COLUMN "wechat_bot_contact"."remark" IS '备注';
COMMENT ON TABLE "wechat_bot_contact" IS '联系人表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "wechat_bot_contact";"""
