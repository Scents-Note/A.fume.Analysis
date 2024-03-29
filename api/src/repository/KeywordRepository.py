from api.src.internal.sql.SqlUtil import SQLUtil

sql_util = SQLUtil.instance()

class KeywordRepository:

    @staticmethod
    def get_keyword_idx_by_name(name):
        sql = 'SELECT id FROM keywords WHERE name="{}"'.format(name)
        result = sql_util.execute(sql=sql)
        if len(result) == 0:
            raise RuntimeError("Wrong keyword name:[{}]".format(name))
        return result[0]['id']

    @staticmethod
    def get_keyword_by_idx(keyword_idx):
        sql = 'SELECT * FROM keywords WHERE id={}'.format(keyword_idx)
        result = sql_util.execute(sql=sql)
        if len(result) == 0:
            raise RuntimeError("Wrong keyword idx:[{}]".format(keyword_idx))
        return result[0]

    @staticmethod
    def get_keywords_by_idx_list(keyword_idx_list: [int]) -> str:
        if len(keyword_idx_list) == 0:
            return ""
        sql = "SELECT name FROM keywords WHERE id IN ({})".format(','.join(map(str, keyword_idx_list)))
        result = sql_util.execute(sql=sql)
        return ','.join(map(lambda x: x['name'], result))
