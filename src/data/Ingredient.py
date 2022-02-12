class Ingredient:

    def __init__(self, idx, name, english_name, description, image_url, series_idx):
        self.idx = idx
        self.name = name
        self.english_name = english_name
        self.description = description
        self.image_url = image_url
        self.series_idx = series_idx

    def __str__(self):
        return 'Ingredient({}, {}, {}, {}, {}, {})'.format(self.idx, self.name, self.english_name,
                                                       self.description, self.image_url, self.series_idx)
