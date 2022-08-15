import abc


class SqlEntity(abc.ABC):

    @abc.abstractmethod
    def get_primary_keys(self) -> [str]:
        pass

    @abc.abstractmethod
    def get_table_name(self) -> str:
        pass

    def get_ids(self) -> [int]:
        return [self.__dict__[pk] for pk in self.get_primary_keys()]

    def generate_update_condition(self) -> (str, [any]):
        dic = self.__dict__
        keys = filter(lambda key: key not in self.get_primary_keys() and dic[key] is not None, dic.keys())
        condition_str = ', '.join(['{} = {}'.format(key, '%d' if dic[key].isnumeric() else '%s') for key in keys])
        value_list = [dic[key] for key in keys]
        return condition_str, value_list

    def generate_primary_key_condition(self) -> (str, [any]):
        dic = self.__dict__
        keys = self.get_primary_keys()
        condition_str = ', '.join(['{} = {}'.format(pk, '%d') for pk in keys])
        value_list = [dic[key] for key in keys]
        return condition_str, value_list
