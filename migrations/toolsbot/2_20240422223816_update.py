from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wechat_bot" RENAME COLUMN "nickname" TO "name";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wechat_bot" RENAME COLUMN "name" TO "nickname";"""
