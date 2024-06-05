from motor import motor_asyncio

from config import settings


class MongoConnection:
    def __init__(self):
        self.client = motor_asyncio.AsyncIOMotorClient(f'mongodb://{settings.MONGO_HOST}:{settings.MONGO_PORT}')
        self.db = self.client[settings.DB_NAME]
        self.collection = self.db.get_collection(settings.DB_COLLECTION)


mongodb = MongoConnection()
