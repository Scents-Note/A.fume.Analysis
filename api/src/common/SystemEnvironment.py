import os

import dotenv

from api.src.common.Object import Singleton


class SystemEnvironment(Singleton):

    def __init__(self, env_path: str = os.getenv('ENV_PATH')):
        super().__init__()
        if env_path is None:
            base_dir = os.path.abspath(os.path.dirname(__file__))
            env_path = os.path.join(base_dir, './../../../.env')
        print("env_path is {}".format(env_path))
        dotenv.load_dotenv(dotenv_path=env_path)

    @staticmethod
    def __getenv(key: str, default_value: any = None) -> any:
        x = os.getenv(key)

        if x is not None:
            return x

        if default_value is None:
            raise RuntimeError('{} must be not null'.format(key))

        return default_value

    def getenv_str(self, key: str, default_value: str = None) -> str:
        return self.__getenv(key, default_value)

    def getenv_int(self, key: str, default_value: int = None) -> int:
        return int(self.__getenv(key, default_value))
