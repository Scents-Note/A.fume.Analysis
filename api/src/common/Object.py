import abc


class Singleton(abc.ABC):

    def __init__(self):
        pass

    __instance = None

    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls):
        cls.__instance = cls()
        cls.instance = cls.__get_instance
        return cls.__instance
