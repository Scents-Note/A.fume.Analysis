from api.src.Config import Config
from api.src.internal.entity.SqlEntity import SqlEntity
from api.src.internal.sql.SQLUtil import SQLUtil


class CrudRepository:

    @staticmethod
    def create(entity: SqlEntity):

        entity.generate_update_condition()
        update_query, update_values = entity.generate_update_condition()
        dic = entity.__dict__
        keys = dic.keys()

        sql = 'INSERT {}({}) VALUES({}) ON DUPLICATE KEY UPDATE {}' \
            .format(entity.get_table_name(),
                    ", ".join(keys),
                    ", ".join(['%d' if dic[key].isnumeric() else '%s' for key in keys]),
                    update_query)
        value_list = [update_values]
        result = SQLUtil.instance().execute(sql=sql, args=value_list)
        return result

    @staticmethod
    def read(idx: int):
        raise "un supported api"

    @staticmethod
    def update(entity: SqlEntity):
        if Config.instance().READ_ONLY:
            raise "Because current is READ_ONLY mode, so it can't delete query"
        update_query, update_values = entity.generate_update_condition()
        primary_key_query, primary_key_values = entity.generate_primary_key_condition()

        sql_query = 'UPDATE {} SET {} WHERE {}'.format(entity.get_table_name(), update_query,
                                                       primary_key_query)
        value_list = update_values + primary_key_values
        SQLUtil.instance().execute(sql=sql_query, args=value_list)

    @staticmethod
    def delete(entity: SqlEntity):
        if Config.instance().READ_ONLY:
            raise "Because current is READ_ONLY mode, so it can't delete query"
        primary_key_query, primary_key_values = entity.generate_primary_key_condition()

        sql_query = 'DELETE FROM {} WHERE {}' \
            .format(entity.get_table_name(),
                    primary_key_query)
        SQLUtil.instance().execute(sql=sql_query, args=primary_key_values)
