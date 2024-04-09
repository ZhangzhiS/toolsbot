from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE UNIQUE INDEX "uid_wechat_bot_wxid_b1ec83" ON "wechat_bot" ("wxid");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_wechat_bot_wxid_b1ec83";"""
