import certifi
from pymongo import MongoClient

from api.src.common.Object import Singleton
from api.src.internal.mongo.MongoConfig import MongoConfig


class MongoDB(Singleton):

    def __init__(self):
        super().__init__()
        mongo_uri = MongoConfig.instance().MONGO_URI
        self.client = MongoClient(mongo_uri, tlsCAFile=certifi.where())

    def get_db_list(self) -> [str]:
        return self.client.list_database_names()

    def get_db(self, db_name: str):
        return self.client.get_database(db_name)


if __name__ == '__main__':
    db = MongoDB.instance().get_db('production')
    collection = db.get_collection('users')
    print([it for it in collection.find()])
