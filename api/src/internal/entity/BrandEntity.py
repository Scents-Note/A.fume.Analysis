class BrandEntity:

    def __init__(self, brand_idx: int, name: str, english_name: str, first_initial: str, description: str,
                 image_url: str):
        self.brand_idx = brand_idx
        self.name = name
        self.english_name = english_name
        self.first_initial = first_initial
        self.description = description
        self.image_url = image_url
