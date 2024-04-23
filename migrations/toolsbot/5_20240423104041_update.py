from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "webhook_auth" ALTER COLUMN "token" TYPE VARCHAR(255) USING "token"::VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "webhook_auth" ALTER COLUMN "token" TYPE VARCHAR(64) USING "token"::VARCHAR(64);"""
