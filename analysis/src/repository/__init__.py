import pandas as pd

from api.src.service import PerfumeService


def get_perfume_ingredient_info_list() -> pd.DataFrame:
    return PerfumeService.get_perfume_ingredient_info_list()


def __main():
    return get_perfume_ingredient_info_list()


if __name__ == '__main__':
    print(__main())
