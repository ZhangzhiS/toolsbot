import motor.motor_asyncio
client = motor.motor_asyncio.AsyncIOMotorClient(
    "82.156.173.222",
    27017
)


db = client["test_database"]
