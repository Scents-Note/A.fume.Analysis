import pandas as pd

from api.src.service import PerfumeService
from api.src.service import UserService


def get_perfume_ingredient_info_list() -> pd.DataFrame:
    return PerfumeService.get_perfume_ingredient_info_list()


def get_user_info_list() -> pd.DataFrame:
    return UserService.get_user_info_list()


def get_survey_info_list() -> pd.DataFrame:
    return UserService.get_user_survey_info_list()


def __main():
    return get_perfume_ingredient_info_list()


if __name__ == '__main__':
    print(__main())
