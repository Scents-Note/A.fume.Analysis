from typing import List

from api.src.data.Survey import Survey
from api.src.internal.entity.SurveyEntity import SurveyEntity
from api.src.internal.mongo.MongoDB import MongoDB

cached_series_idx: dict = {}

db = MongoDB.instance().get_db('production')


class SurveyRepository:

    @staticmethod
    def get_survey_all() -> List[Survey]:
        entity_list = [SurveyEntity.create(it) for it in db.get_collection('users').find()]
        return [Survey(_id=it._id, user_idx=it.user_idx, keyword_list=it.survey_keyword_list,
                       perfume_list=it.survey_perfume_list, series_list=it.survey_series_list) for it in
                entity_list]


if __name__ == '__main__':
    print(list(map(str, SurveyRepository.get_survey_all())))
