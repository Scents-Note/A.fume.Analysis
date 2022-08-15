from typing import List

from api.src.data.Series import Series
from api.src.internal.sql.SQLUtil import SQLUtil


class SeriesRepository:

    @staticmethod
    def get_series_all() -> List[Series]:
        sql = 'SELECT * FROM series'

        SQLUtil.instance().execute(sql=sql)
        return [Series(idx=it['series_idx'], name=it['name'], description=it['description'])
                for it in SQLUtil.instance().fetchall()]


def main():
    SQLUtil.instance().logging = True

    SeriesRepository.get_series_all()


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
