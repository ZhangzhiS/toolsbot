from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wechat_bot" RENAME COLUMN "api_host" TO "callback_url";
        ALTER TABLE "wechat_bot" ALTER COLUMN "token" DROP NOT NULL;
        ALTER TABLE "wechat_bot" ALTER COLUMN "nickname" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wechat_bot" RENAME COLUMN "callback_url" TO "api_host";
        ALTER TABLE "wechat_bot" ALTER COLUMN "token" SET NOT NULL;
        ALTER TABLE "wechat_bot" ALTER COLUMN "nickname" SET NOT NULL;"""
