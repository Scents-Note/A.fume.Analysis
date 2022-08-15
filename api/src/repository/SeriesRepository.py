from typing import List

from api.src.data.Series import Series
from api.src.internal.sql.SqlUtil import SQLUtil

cached_series_idx: dict = {}


class SeriesRepository:

    @staticmethod
    def get_series_all() -> List[Series]:
        sql = 'SELECT * FROM series'

        SQLUtil.instance().execute(sql=sql)
        return [Series(idx=it['series_idx'], name=it['name'], description=it['description'])
                for it in SQLUtil.instance().fetchall()]

    @staticmethod
    def get_series_idx(name: str) -> int:
        if name in cached_series_idx:
            return cached_series_idx[name]

        sql = 'SELECT series_idx FROM series WHERE name = %s'
        SQLUtil.instance().execute(sql, [name])
        result = SQLUtil.instance().fetchall()
        if len(result) == 0:
            raise RuntimeError('name[{}] is not a name of series'.format(name))
        if len(result) > 1:
            raise RuntimeError('name[{}] has more than one series'.format(name))
        series_idx = result[0]['series_idx']
        cached_series_idx[name] = series_idx
        return series_idx


def main():
    SQLUtil.instance().logging = True

    SeriesRepository.get_series_all()


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
