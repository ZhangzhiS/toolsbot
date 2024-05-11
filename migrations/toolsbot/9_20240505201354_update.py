from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "positionidmap" ALTER COLUMN "withdrawal_amount" SET DEFAULT '0';
        ALTER TABLE "positionidmap" ALTER COLUMN "withdrawal_amount" TYPE DECIMAL(10,2) USING "withdrawal_amount"::DECIMAL(10,2);
        ALTER TABLE "positionidmap" ALTER COLUMN "withdrawal_amount" TYPE DECIMAL(10,2) USING "withdrawal_amount"::DECIMAL(10,2);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "positionidmap" ALTER COLUMN "withdrawal_amount" TYPE INT USING "withdrawal_amount"::INT;
        ALTER TABLE "positionidmap" ALTER COLUMN "withdrawal_amount" SET DEFAULT 0;"""
