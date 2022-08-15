from api.src.internal.entity.SqlEntity import SqlEntity


class SeriesEntity(SqlEntity):

    def __init__(self, series_idx: int, name: str, english_name: str, description: str, image_url: str):
        self.series_idx = series_idx
        self.name = name
        self.english_name = english_name
        self.description = description
        self.image_url = image_url

    def get_primary_keys(self) -> [str]:
        return ['series_idx']

    def get_table_name(self) -> str:
        return 'series'
