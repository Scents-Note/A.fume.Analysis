from api.src.common.SystemEnvironment import SystemEnvironment


class Config(SystemEnvironment):

    def __init__(self):
        super().__init__()

        self.MYSQL_USER = self.getenv_str('MYSQL_USER')
        self.MYSQL_PASSWD = self.getenv_str('MYSQL_PASSWD')
        self.MYSQL_DB = self.getenv_str('MYSQL_DB')
        self.MYSQL_HOST = self.getenv_str('MYSQL_HOST')
        self.MYSQL_CHARSET = self.getenv_str('MYSQL_CHARSET')
        self.MYSQL_PORT = self.getenv_int('MYSQL_PORT')

