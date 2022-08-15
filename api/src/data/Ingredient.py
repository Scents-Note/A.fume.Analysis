class Ingredient:

    def __init__(self, idx: int, name: str, description: str, image_url: str, series_idx: int):
        self.idx = idx
        self.name = name
        self.description = description
        self.image_url = image_url
        self.series_idx = series_idx

    def __str__(self):
        return 'Ingredient({}, {}, {}, {}, {}, {})'.format(self.idx, self.name,
                                                           self.description, self.image_url, self.series_idx)
