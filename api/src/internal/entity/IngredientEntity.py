class IngredientEntity:

    def __init__(self, ingredient_idx: int, name: str, description: str, image_url: str,
                 series_idx: int, category_idx: int):
        self.ingredient_idx = ingredient_idx
        self.name = name
        self.description = description
        self.image_url = image_url
        self.series_idx = series_idx
        self.category_idx = category_idx

    @staticmethod
    def create(data: dict):
        return IngredientEntity(ingredient_idx=data['ingredient_idx'], name=data['name'],
                                description=data['description'],
                                image_url=data['image_url'],
                                series_idx=data['series_idx'],
                                category_idx=data['category_idx'])