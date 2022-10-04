import abc

from api.src.Config import Config
from api.src.common.Object import Singleton
from api.src.internal.entity.BrandEntity import BrandEntity
from api.src.internal.entity.SeriesEntity import SeriesEntity
from api.src.internal.sql.SqlUtil import SQLUtil

sql_util = SQLUtil.instance()


class SqlModel(Singleton, abc.ABC):

    def read_all(self) -> [any]:
        sql = "SELECT * FROM {}".format(self.get_table_name())
        return sql_util.execute(sql=sql)

    def create(self, data: dict):
        update_query, update_values = self.__generate_update_condition(data)
        if len(update_values) == 0:
            return

        keys = data.keys()

        sql = 'INSERT {}({}) VALUES({}) ON DUPLICATE KEY UPDATE {}' \
            .format(self.get_table_name(),
                    ", ".join(keys),
                    ", ".join(['%s' for _ in keys]),
                    update_query)
        value_list = [data[key] for key in keys] + update_values
        return sql_util.execute(sql=sql, args=value_list)

    def readByPk(self, data: dict) -> any:
        primary_key_query, primary_key_values = self.__generate_primary_key_condition(data)

        sql_query = 'SELECT * FROM {} WHERE {}'.format(self.get_table_name(), primary_key_query)
        value_list = primary_key_values
        return sql_util.execute(sql=sql_query, args=value_list)

    def update(self, data: dict) -> int:
        if Config.instance().READ_ONLY:
            raise "Because current is READ_ONLY mode, so it can't delete query"
        update_query, update_values = self.__generate_update_condition(data)
        if len(update_values) == 0:
            return 0
        primary_key_query, primary_key_values = self.__generate_primary_key_condition(data)

        sql_query = 'UPDATE {} SET {} WHERE {}'.format(self.get_table_name(), update_query,
                                                       primary_key_query)
        value_list = update_values + primary_key_values
        affected_rows = sql_util.execute(sql=sql_query, args=value_list)
        return affected_rows

    def delete(self, data: dict):
        if Config.instance().READ_ONLY:
            raise "Because current is READ_ONLY mode, so it can't delete query"
        primary_key_query, primary_key_values = self.__generate_primary_key_condition(data, delimiter=" AND ")

        sql_query = 'DELETE FROM {} WHERE {}' \
            .format(self.get_table_name(),
                    primary_key_query)
        sql_util.execute(sql=sql_query, args=primary_key_values)

    @abc.abstractmethod
    def get_primary_keys(self) -> [str]:
        pass

    @abc.abstractmethod
    def get_table_name(self) -> str:
        pass

    def __get_ids(self) -> [int]:
        return [self.__dict__[pk] for pk in self.get_primary_keys()]

    def __generate_update_condition(self, data: dict) -> (str, [any]):
        keys = list(filter(lambda key: key not in self.get_primary_keys() and data[key] is not None, data.keys()))
        condition_str = ', '.join(['{} = {}'.format(key, '%s') for key in keys])
        value_list = [data[key] for key in keys]
        return condition_str, value_list

    def __generate_primary_key_condition(self, dic: dict, delimiter=', ') -> (str, [any]):
        keys = self.get_primary_keys()
        condition_str = delimiter.join(['{} = {}'.format(pk, '%s') for pk in keys])
        value_list = [dic[key] for key in keys]
        return condition_str, value_list


class BrandModel(SqlModel):

    def read_all(self) -> [BrandEntity]:
        result = super().read_all()
        return [BrandEntity.create(row) for row in result]

    def get_table_name(self) -> str:
        return 'brands'

    def get_primary_keys(self) -> [str]:
        return ['brand_idx']


class SeriesModel(SqlModel):

    def read_all(self) -> [SeriesEntity]:
        result = super().read_all()
        return [SeriesEntity.create(row) for row in result]

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
        return ['ingredient_idx']

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
