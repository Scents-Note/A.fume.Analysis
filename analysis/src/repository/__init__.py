import numpy as np
import pandas as pd


# TODO 함수 이름은 적절 하게 변경 하셔도 됩니다.
def get_perfume_ingredient_info_list() -> pd.DataFrame:
    dummy = np.array([
        [1, '향수1', "['계열1', '계열2']", "['재료1', '재료2', '재료3']", "['카테고리1', '카테고리2', '카테고리3']"],
        [2, '향수2', "['계열3', '계열4']", "['재료3', '재료2', '재료5']", "['카테고리3', '카테고리8', '카테고리5']"],
        [4, '향수4', "['계열3', '계열6']", "['재료3', '재료5', '재료7']", "['카테고리3', '카테고리7', '카테고리3']"]
    ])
    df = pd.DataFrame(data=dummy, index=[1, 2, 4], columns=[
        'perfume_idx', 'perfume_name', 'series_name_list', 'ingredients_name_list', 'category_name_list'
    ])
    return df


def __main():
    return get_perfume_ingredient_info_list()


if __name__ == '__main__':
    print(__main())
