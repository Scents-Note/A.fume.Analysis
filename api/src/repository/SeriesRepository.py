from typing import List

from api.src.data.Series import Series
from api.src.internal.sql.SqlUtil import SQLUtil

cached_series_idx: dict = {}

sql_util = SQLUtil.instance()
class SeriesRepository:

    @staticmethod
    def get_series_all() -> List[Series]:
        sql = 'SELECT * FROM series'

        result = sql_util.execute(sql=sql)
        return [Series(idx=it['series_idx'], name=it['name'], description=it['description'])
                for it in result]

    @staticmethod
    def get_series_idx(name: str) -> int:
        if name in cached_series_idx:
            return cached_series_idx[name]

        sql = 'SELECT series_idx FROM series WHERE name = %s'
        result = sql_util.execute(sql, [name])
        if len(result) == 0:
            raise RuntimeError('name[{}] is not a name of series'.format(name))
        if len(result) > 1:
            raise RuntimeError('name[{}] has more than one series'.format(name))
        series_idx = result[0]['series_idx']
        cached_series_idx[name] = series_idx
        return series_idx


def main():
    sql_util.logging = True
    sql_util.debug = True
    SeriesRepository.get_series_all()


if __name__ == '__main__':
    main()
