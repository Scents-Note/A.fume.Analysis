import os
from dotenv import load_dotenv

from src.common.Strings import CommandInfo


def getenvNonNull(key) -> any:
    x = os.getenv(key)
    if x is None:
        raise RuntimeError('{} must be not null'.format(key))
    return x


class Config:

    def __init__(self):
        import os
        load_dotenv(dotenv_path='../../.env')

        self.INPUT_DIR_PATH = os.getenv('INPUT_DIR_PATH') or './input'
        self.OUTPUT_DIR_PATH = os.getenv('OUTPUT_DIR_PATH') or './output'
        self.DEBUG = os.getenv('DEBUG').lower() == 'true'
        self.TARGET = os.getenv('TARGET') or '*'
        self.COMMAND = getenvNonNull('COMMAND')

    def get_target_list(self) -> [str]:
        if self.TARGET == '*':
            return [CommandInfo.brand, CommandInfo.series, CommandInfo.perfume, CommandInfo.ingredient]
        return self.TARGET.split(',')

    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls):
        cls.__instance = cls()
        cls.instance = cls.__getInstance
        return cls.__instance
