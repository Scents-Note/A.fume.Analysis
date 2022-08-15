class IngredientEntity:

    def __init__(self, ingredient_idx: int, name: str, english_name: str, description: str, image_url: str,
                 series_idx: int, category_idx: int):
        self.ingredient_idx = ingredient_idx
        self.name = name
        self.english_name = english_name
        self.description = description
        self.image_url = image_url
        self.series_idx = series_idx
        self.category_idx = category_idx
