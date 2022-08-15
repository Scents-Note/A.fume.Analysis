class Ingredient:

    def __init__(self, idx: int, name: str, description: str, image_url: str, series_idx: int):
        self.idx = idx
        self.name = name
        self.description = description
        self.image_url = image_url
        self.series_idx = series_idx

    def __str__(self):
        return 'Ingredient({}, {}, {}, {}, {})'.format(self.idx, self.name,
                                                       self.description, self.image_url, self.series_idx)


class IngredientInfo:
    def __init__(self, idx: int, name: str, description: str, series_idx: int, series_name: str, category_idx: int,
                 category_name: str, image_url: str):
        self.idx = idx
        self.name = name
        self.description = description
        self.series_idx = series_idx
        self.series_name = series_name
        self.category_idx = category_idx
        self.category_name = category_name
        self.image_url = image_url

    @staticmethod
    def create(data: dict):
        return IngredientInfo(idx=data['idx'], name=data['name'], description=data['description'],
                              series_idx=data['series_idx'], series_name=data['series_name'],
                              category_idx=data['category_idx'], category_name=data['category_name'],
                              image_url=data['image_url'])
