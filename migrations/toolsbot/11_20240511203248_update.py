from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "positionidmap" ADD "take_a_percentage" VARCHAR(3) NOT NULL  DEFAULT '15';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "positionidmap" DROP COLUMN "take_a_percentage";"""
