from api.src.common.SystemEnvironment import SystemEnvironment
from rawfile.src.common.Strings import CommandInfo


class Config(SystemEnvironment):

    def __init__(self):
        super(Config, self).__init__()

        self.INPUT_DIR_PATH = self.getenv_str('INPUT_DIR_PATH', './input')
        self.OUTPUT_DIR_PATH = self.getenv_str('OUTPUT_DIR_PATH', './output')
        self.DEBUG = self.getenv_str('DEBUG', 'false').lower() == 'true'
        self.TARGET = self.getenv_str('TARGET', '*')
        self.COMMAND = self.getenv_str('COMMAND')

    def get_target_list(self) -> [str]:
        if self.TARGET == '*':
            return [CommandInfo.brand, CommandInfo.series, CommandInfo.perfume, CommandInfo.ingredient]
        return self.TARGET.split(',')
