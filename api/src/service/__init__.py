import numpy as np
import pandas as pd

from api.src.common.Object import Singleton
from api.src.internal.entity.PerfumeEntity import PerfumeEntity
from api.src.internal.sql.SqlUtil import SQLUtil
from api.src.repository.KeywordRepository import KeywordRepository
from api.src.repository.SeriesRepository import SeriesRepository
from api.src.repository.SurveyRepository import SurveyRepository

COL_PERFUME_IDX = 'perfume_idx'
COL_PERFUME_NAME = 'perfume_name'
COL_PERFUME_ENGLISH_NAME = 'perfume_english_name'
COL_PERFUME_STORY = 'perfume_story'
COL_PERFUME_VOLUME_AND_PRICE = 'perfume_volume_and_price'
COL_PERFUME_ABUNDANCE_RATE = 'perfume_abundance_rate'
COL_BRAND_IDX = 'brand_idx'
COL_BRAND_NAME = 'brand_name'
COL_BRAND_ENGLISH_NAME = 'brand_english_name'
COL_INGREDIENT_NAME_LIST = 'ingredient_name_list'
COL_CATEGORY_NAME_LIST = 'category_name_list'
COL_SERIES_NAME_LIST = 'series_name_list'

COL_USER_IDX = 'user_idx'
COL_USER_NICKNAME = 'nickname'
COL_USER_EMAIL = 'email'
COL_USER_GENDER = 'gender'
COL_USER_BIRTH = 'birth_year'
COL_CREATED_AT = 'created_at'
COL_ACCESS_TIME = 'access_time'
COL_USER_LIKE_PERFUME_LIST = 'liked_perfume_idx_list'
COL_USER_REVIEWED_PERFUME_LIST = 'reviewed_perfume_list'

COL_SURVEY_PERFUME_LIST = 'survey_perfume_idx_list'
COL_SURVEY_SERIES_LIST = 'survey_series_list'
COL_SURVEY_KEYWORD_LIST = 'survey_keyword_list'


def convert_to_array(text: str) -> str:
    if text is None:
        return ""
    return str(sorted(text.split(',')))


class PerfumeService(Singleton):

    @staticmethod
    def get_perfume_ingredient_info_list() -> pd.DataFrame:
        sql_util = SQLUtil.instance()
        sql = "SELECT p.perfume_idx as '{}', p.name as '{}', " \
              "p.english_name as '{}', " \
              "p.story as '{}', " \
              "p.volume_and_price as '{}', " \
              "p.abundance_rate as '{}', " \
              "b.brand_idx as '{}', " \
              "b.name as '{}', " \
              "b.english_name as '{}', " \
              "GROUP_CONCAT(DISTINCT(i.name)) AS '{}', " \
              "GROUP_CONCAT(DISTINCT(ic.name)) AS '{}', " \
              "GROUP_CONCAT(DISTINCT(s.name)) AS '{}' " \
              "FROM perfumes AS p " \
              "LEFT JOIN brands AS b " \
              "ON p.brand_idx = b.brand_idx " \
              "LEFT JOIN notes AS n " \
              "ON p.perfume_idx = n.perfume_idx " \
              "LEFT JOIN ingredients AS i " \
              "ON n.ingredient_idx = i.ingredient_idx " \
              "LEFT JOIN series as s " \
              "ON s.series_idx = i.series_idx " \
              "LEFT JOIN ingredient_categories AS ic " \
              "ON i.category_idx = ic.id " \
              "WHERE p.deleted_at is NULL " \
              "GROUP BY p.perfume_idx ".format(COL_PERFUME_IDX, COL_PERFUME_NAME, COL_PERFUME_ENGLISH_NAME,
                                               COL_PERFUME_STORY, COL_PERFUME_VOLUME_AND_PRICE,
                                               COL_PERFUME_ABUNDANCE_RATE,
                                               COL_BRAND_IDX,
                                               COL_BRAND_NAME,
                                               COL_BRAND_ENGLISH_NAME,
                                               COL_INGREDIENT_NAME_LIST,
                                               COL_CATEGORY_NAME_LIST, COL_SERIES_NAME_LIST)
        result = sql_util.execute(sql=sql)

        dummy = np.array(
            [
                [
                    item[COL_PERFUME_IDX],
                    item[COL_PERFUME_NAME],
                    item[COL_PERFUME_ENGLISH_NAME],
                    item[COL_PERFUME_VOLUME_AND_PRICE],
                    item[COL_PERFUME_STORY],
                    PerfumeEntity.abundance_rate_list[item[COL_PERFUME_ABUNDANCE_RATE]],
                    item[COL_BRAND_IDX],
                    item[COL_BRAND_NAME],
                    item[COL_BRAND_ENGLISH_NAME],
                    convert_to_array(item[COL_SERIES_NAME_LIST]),
                    convert_to_array(item[COL_INGREDIENT_NAME_LIST]),
                    convert_to_array(item[COL_CATEGORY_NAME_LIST])
                ] for item in result
            ])
        index = list(map(lambda it: it[COL_PERFUME_IDX], result))
        df = pd.DataFrame(data=dummy, index=index, columns=[
            COL_PERFUME_IDX, COL_PERFUME_NAME, COL_PERFUME_ENGLISH_NAME, COL_PERFUME_VOLUME_AND_PRICE,
            COL_PERFUME_STORY, COL_PERFUME_ABUNDANCE_RATE,
            COL_BRAND_IDX, COL_BRAND_NAME, COL_BRAND_ENGLISH_NAME,
            COL_SERIES_NAME_LIST, COL_INGREDIENT_NAME_LIST, COL_CATEGORY_NAME_LIST
        ])
        return df


class UserService(Singleton):

    # 회원 정보
    # - 하트 누른 향수: liked_perfume_idx_list [perfume_idx, ...]
    # - 향수 별점 준 현황: reviewed_perfume_list e.g) [perfume_idx:score,...]
    @staticmethod
    def get_user_info_list() -> pd.DataFrame:
        sql_util = SQLUtil.instance()
        sql = "SELECT u.user_idx as '{}', u.nickname as '{}', " \
              "u.email as '{}', " \
              "u.gender as '{}', " \
              "u.birth as '{}', " \
              "u.created_at as '{}', " \
              "u.access_time as '{}', " \
              "GROUP_CONCAT(DISTINCT(lp.perfume_idx)) AS '{}', " \
              "GROUP_CONCAT(DISTINCT(r.perfume_idx), \":\", r.score) AS '{}' " \
              "FROM users u " \
              "LEFT JOIN like_perfumes AS lp " \
              "ON u.user_idx = lp.user_idx " \
              "LEFT JOIN reviews AS r " \
              "ON u.user_idx = r.user_idx " \
              "WHERE u.deleted_at IS NULL " \
              "AND r.deleted_at IS NULL " \
              "GROUP BY u.user_idx ".format(COL_USER_IDX, COL_USER_NICKNAME, COL_USER_EMAIL,
                                            COL_USER_GENDER, COL_USER_BIRTH,
                                            COL_CREATED_AT, COL_ACCESS_TIME,
                                            COL_USER_LIKE_PERFUME_LIST,
                                            COL_USER_REVIEWED_PERFUME_LIST)
        result = sql_util.execute(sql=sql)
        datas = np.array(
            [
                [
                    item[COL_USER_IDX],
                    item[COL_USER_NICKNAME],
                    item[COL_USER_EMAIL],
                    item[COL_USER_GENDER],
                    item[COL_USER_BIRTH],
                    item[COL_CREATED_AT].isoformat(),
                    item[COL_ACCESS_TIME].isoformat(),
                    convert_to_array(item[COL_USER_LIKE_PERFUME_LIST]),
                    convert_to_array(item[COL_USER_REVIEWED_PERFUME_LIST])
                ] for item in result
            ])
        index = list(map(lambda it: it[COL_USER_IDX], result))
        df = pd.DataFrame(data=datas, index=index, columns=[
            COL_USER_IDX, COL_USER_NICKNAME, COL_USER_EMAIL, COL_USER_GENDER,
            COL_USER_BIRTH, COL_CREATED_AT,
            COL_ACCESS_TIME, COL_USER_LIKE_PERFUME_LIST, COL_USER_REVIEWED_PERFUME_LIST
        ])
        return df


    @staticmethod
    def get_user_survey_info_list() -> pd.DataFrame:
        surveys = SurveyRepository.get_survey_all()

        datas = np.array(
            [
                [
                    item.user_idx,
                    str(item.perfume_list),
                    SeriesRepository.get_series_by_idx_list(item.series_list),
                    KeywordRepository.get_keywords_by_idx_list(item.keyword_list),
                ] for item in surveys
            ])
        index = list(map(lambda it: it.user_idx, surveys))
        df = pd.DataFrame(data=datas, index=index, columns=[
            COL_USER_IDX, COL_SURVEY_PERFUME_LIST, COL_SURVEY_SERIES_LIST, COL_SURVEY_KEYWORD_LIST
        ])
        return df


def __main():
    # return PerfumeService.instance().get_perfume_ingredient_info_list()
    return UserService.instance().get_user_info_list()


def testPerfumeInfoList():
    res = PerfumeService.instance().get_perfume_ingredient_info_list()

    file_nm = "temp.xlsx"

    res.to_excel("./{}".format(file_nm),
                 sheet_name='temp',
                 na_rep='',
                 float_format="%.2f",
                 header=True,
                 index=False,
                 index_label="id",
                 startrow=1,
                 startcol=1,
                 # engine = 'xlsxwriter',
                 freeze_panes=(2, 0)
                 )


def testUserInfoList():
    res = UserService.instance().get_user_survey_info_list()

    file_nm = "temp.xlsx"

    res.to_excel("./{}".format(file_nm),
                 sheet_name='temp',
                 na_rep='',
                 float_format="%.2f",
                 header=True,
                 index=False,
                 index_label="user_idx",
                 startrow=1,
                 startcol=1,
                 # engine = 'xlsxwriter',
                 freeze_panes=(2, 0)
                 )


if __name__ == '__main__':
    testUserInfoList()
