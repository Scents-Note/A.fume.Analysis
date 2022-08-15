import abc

from api.src.Config import Config
from api.src.common.Object import Singleton
from api.src.internal.sql.SQLUtil import SQLUtil


class SqlModel(Singleton, abc.ABC):

    def create(self, data: dict):
        update_query, update_values = self.__generate_update_condition(data)
        keys = data.keys()

        sql = 'INSERT {}({}) VALUES({}) ON DUPLICATE KEY UPDATE {}' \
            .format(self.get_table_name(),
                    ", ".join(keys),
                    ", ".join(['%d' if data[key].isnumeric() else '%s' for key in keys]),
                    update_query)
        value_list = [update_values]
        result = SQLUtil.instance().execute(sql=sql, args=value_list)
        return result

    def readByPk(self, data: dict) -> any:
        primary_key_query, primary_key_values = self.__generate_primary_key_condition(data)

        sql_query = 'SELECT * FROM {} WHERE {}'.format(self.get_table_name(), primary_key_query)
        value_list = primary_key_values
        SQLUtil.instance().execute(sql=sql_query, args=value_list)
        return SQLUtil.instance().fetchall()[0]

    def update(self, data: dict):
        if Config.instance().READ_ONLY:
            raise "Because current is READ_ONLY mode, so it can't delete query"
        update_query, update_values = self.__generate_update_condition(data)
        primary_key_query, primary_key_values = self.__generate_primary_key_condition(data)

        sql_query = 'UPDATE {} SET {} WHERE {}'.format(self.get_table_name(), update_query,
                                                       primary_key_query)
        value_list = update_values + primary_key_values
        SQLUtil.instance().execute(sql=sql_query, args=value_list)

    def delete(self, data: dict):
        if Config.instance().READ_ONLY:
            raise "Because current is READ_ONLY mode, so it can't delete query"
        primary_key_query, primary_key_values = self.__generate_primary_key_condition(data)

        sql_query = 'DELETE FROM {} WHERE {}' \
            .format(self.get_table_name(),
                    primary_key_query)
        SQLUtil.instance().execute(sql=sql_query, args=primary_key_values)

    @abc.abstractmethod
    def get_primary_keys(self) -> [str]:
        pass

    @abc.abstractmethod
    def get_table_name(self) -> str:
        pass

    def __get_ids(self) -> [int]:
        return [self.__dict__[pk] for pk in self.get_primary_keys()]

    def __generate_update_condition(self, dic: dict) -> (str, [any]):
        keys = filter(lambda key: key not in self.get_primary_keys() and dic[key] is not None, dic.keys())
        condition_str = ', '.join(['{} = {}'.format(key, '%d' if dic[key].isnumeric() else '%s') for key in keys])
        value_list = [dic[key] for key in keys]
        return condition_str, value_list

    def __generate_primary_key_condition(self, dic: dict) -> (str, [any]):
        keys = self.get_primary_keys()
        condition_str = ', '.join(['{} = {}'.format(pk, '%d') for pk in keys])
        value_list = [dic[key] for key in keys]
        return condition_str, value_list


class BrandModel(SqlModel):

    def get_table_name(self) -> str:
        return 'brands'

    def get_primary_keys(self) -> [str]:
        return ['brand_idx']


class SeriesModel(SqlModel):

    def get_primary_keys(self) -> [str]:
        return ['series_idx']

    def get_table_name(self) -> str:
        return 'series'


class IngredientCategoryModel(SqlModel):

    def get_primary_keys(self) -> [str]:
        return ['id']

    def get_table_name(self) -> str:
        return 'ingredient_categories'


class IngredientModel(SqlModel):

    def get_primary_keys(self) -> [str]:
        return ['brand_idx']

    def get_table_name(self) -> str:
        return 'ingredients'


class NoteModel(SqlModel):

    def get_primary_keys(self) -> [str]:
        return ['perfume_idx', 'ingredient_idx']

    def get_table_name(self) -> str:
        return 'notes'


class PerfumeModel(SqlModel):

    def get_primary_keys(self) -> [str]:
        return ['perfume_idx']

    def get_table_name(self) -> str:
        return 'perfumes'


brand_model = BrandModel.instance()
series_model = SeriesModel.instance()
ingredient_category_model = IngredientCategoryModel.instance()
ingredient_model = IngredientModel.instance()
note_model = NoteModel.instance()
perfume_model = PerfumeModel.instance()
