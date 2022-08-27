from typing import List

from api.src.data.Perfume import Perfume
from api.src.internal.sql.SqlUtil import SQLUtil

sql_util = SQLUtil.instance()


class PerfumeRepository:

    @staticmethod
    def get_all_perfume() -> List[Perfume]:
        sql = 'SELECT * from perfumes'

        result = sql_util.execute(sql=sql)
        return [
            Perfume(idx=it['perfume_idx'], name=it['name'], english_name=it['english_name'], image_url=it['image_url'],
                    story=it['story'], abundance_rate=it['abundance_rate'], volume_and_price=it['volume_and_price'])
            for it in result]


def main():
    sql_util.logging = True
    sql_util.debug = True
    print(PerfumeRepository.get_all_perfume())


if __name__ == '__main__':
    main()
