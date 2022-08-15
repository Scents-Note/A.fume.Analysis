class SeriesEntity:

    def __init__(self, series_idx: int, name: str, english_name: str, description: str, image_url: str):
        self.series_idx = series_idx
        self.name = name
        self.english_name = english_name
        self.description = description
        self.image_url = image_url

    @staticmethod
    def create(it: dict):
        return SeriesEntity(series_idx=it['series_idx'], name=it['name'],
                            english_name=it['english_name'],
                            image_url=it['image_url'],
                            description=it['description'])
