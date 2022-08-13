import os
from dotenv import load_dotenv


def getenvNonNull(key) -> any:
    x = os.getenv(key)
    if x is None:
        raise RuntimeError('{} must be not null'.format(key))
    return x


class Config:

    def __init__(self):
        load_dotenv(dotenv_path='../../.env')

        self.MYSQL_USER = getenvNonNull('MYSQL_USER')
        self.MYSQL_PASSWD = getenvNonNull('MYSQL_PASSWD')
        self.MYSQL_DB = getenvNonNull('MYSQL_DB')
        self.MYSQL_HOST = getenvNonNull('MYSQL_HOST')
        self.MYSQL_CHARSET = getenvNonNull('MYSQL_CHARSET')
        self.MYSQL_PORT = int(getenvNonNull('MYSQL_PORT'))

    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls):
        cls.__instance = cls()
        cls.instance = cls.__getInstance
        return cls.__instance
