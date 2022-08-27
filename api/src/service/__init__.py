import numpy as np
import pandas as pd

from api.src.common.Object import Singleton
from api.src.internal.sql.SqlUtil import SQLUtil

COL_PERFUME_IDX = 'perfume_idx'
COL_PERFUME_NAME = 'perfume_name'
COL_INGREDIENT_NAME_LIST = 'ingredient_name_list'
COL_CATEGORY_NAME_LIST = 'category_name_list'
COL_SERIES_NAME_LIST = 'series_name_list'


class PerfumeService(Singleton):

    @staticmethod
    def get_perfume_ingredient_info_list() -> pd.DataFrame:
        sql_util = SQLUtil.instance()
        sql = "SELECT p.perfume_idx as '{}', p.name as '{}', " \
              "GROUP_CONCAT(DISTINCT(i.name)) AS '{}', " \
              "GROUP_CONCAT(DISTINCT(ic.name)) AS '{}', " \
              "GROUP_CONCAT(DISTINCT(s.name)) AS '{}' " \
              "FROM perfumes AS p " \
              "INNER JOIN notes AS n " \
              "ON p.perfume_idx = n.perfume_idx " \
              "INNER JOIN ingredients AS i " \
              "ON n.ingredient_idx = i.ingredient_idx " \
              "INNER JOIN series as s " \
              "ON s.series_idx = i.series_idx " \
              "INNER JOIN ingredient_categories AS ic " \
              "ON i.category_idx = ic.id " \
              "GROUP BY p.perfume_idx ".format(COL_PERFUME_IDX, COL_PERFUME_NAME, COL_INGREDIENT_NAME_LIST,
                                               COL_CATEGORY_NAME_LIST, COL_SERIES_NAME_LIST)
        result = sql_util.execute(sql=sql)

        def convert_to_array(text: str) -> str:
            return str(sorted(text.split(',')))

        dummy = np.array(
            [
                [
                    item[COL_PERFUME_IDX],
                    item[COL_PERFUME_NAME],
                    convert_to_array(item[COL_SERIES_NAME_LIST]),
                    convert_to_array(item[COL_INGREDIENT_NAME_LIST]),
                    convert_to_array(item[COL_CATEGORY_NAME_LIST])
                ] for item in result
            ])
        index = list(map(lambda it: it[COL_PERFUME_IDX], result))
        df = pd.DataFrame(data=dummy, index=index, columns=[
            COL_PERFUME_IDX, COL_PERFUME_NAME, COL_SERIES_NAME_LIST, COL_INGREDIENT_NAME_LIST, COL_CATEGORY_NAME_LIST
        ])
        return df


def __main():
    return PerfumeService.instance().get_perfume_ingredient_info_list()


if __name__ == '__main__':
    df = __main()

    # file_nm = "temp.xlsx"

    # df.to_excel("./{}".format(file_nm),
    #             sheet_name='temp',
    #             na_rep='',
    #             float_format="%.2f",
    #             header=True,
    #             index=False,
    #             index_label="id",
    #             startrow=1,
    #             startcol=1,
    #             # engine = 'xlsxwriter',
    #             freeze_panes=(2, 0)
    #             )
    print(df)
