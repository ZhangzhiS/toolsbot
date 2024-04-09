from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wechat_bot" ADD "user_id" VARCHAR(64);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wechat_bot" DROP COLUMN "user_id";"""
