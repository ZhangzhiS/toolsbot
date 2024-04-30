from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "jdrebate" ALTER COLUMN "sku_name" TYPE VARCHAR(255) USING "sku_name"::VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "jdrebate" ALTER COLUMN "sku_name" TYPE VARCHAR(64) USING "sku_name"::VARCHAR(64);"""
