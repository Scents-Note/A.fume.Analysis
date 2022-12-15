from api.src.common.SystemEnvironment import SystemEnvironment


class MongoConfig(SystemEnvironment):

    def __init__(self):
        super().__init__()

        self.MONGO_URI = self.getenv_str('MONGO_URI')
