class BrandEntity:

    def __init__(self, brand_idx: int, name: str, first_initial: str, description: str,
                 image_url: str):
        self.brand_idx = brand_idx
        self.name = name
        self.first_initial = first_initial
        self.description = description
        self.image_url = image_url

    @staticmethod
    def create(data: dict):
        return BrandEntity(brand_idx=data['brand_idx'], name=data['name'],
                           first_initial=data['first_initial'], description=data['description'],
                           image_url=data['image_url'])
