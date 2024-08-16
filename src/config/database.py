import os
import asyncio

import motor.motor_asyncio
from .settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url.strip())
client.get_io_loop = asyncio.get_running_loop

TEST_MODE = bool(int(os.getenv("TEST_MODE", "0")))
db: motor.motor_asyncio.AsyncIOMotorDatabase

if TEST_MODE:
    db = client.test_db
else:
    db = client.product_microservice
