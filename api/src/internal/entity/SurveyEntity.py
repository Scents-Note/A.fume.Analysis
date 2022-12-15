from typing import List


class SurveyEntity:

    def __init__(self, _id: int, user_idx: str, survey_keyword_list: List[int], survey_series_list: List[int],
                 survey_perfume_list: List[int], created_at: str, update_at: str):
        self._id = _id
        self.user_idx = user_idx
        self.survey_keyword_list = survey_keyword_list
        self.survey_series_list = survey_series_list
        self.survey_perfume_list = survey_perfume_list
        self.created_at = created_at
        self.update_at = update_at

    @staticmethod
    def create(it: dict):
        return SurveyEntity(_id=it['_id'], user_idx=it['userIdx'],
                            survey_series_list=it['surveySeriesList'],
                            survey_keyword_list=it['surveyKeywordList'],
                            survey_perfume_list=it['surveyPerfumeList'],
                            created_at=it['createdAt'],
                            update_at=it['updatedAt'])
