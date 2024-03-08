import motor.motor_asyncio
from .settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url.strip())

db: motor.motor_asyncio.AsyncIOMotorDatabase = client.product_microservice