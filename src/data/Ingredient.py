class Ingredient:

    def __init__(self, ingredient_idx, name, english_name, description, image_url):
        self.ingredient_idx = ingredient_idx
        self.name = name
        self.english_name = english_name
        self.description = description
        self.image_url = image_url

    def __str__(self):
        return 'Ingredient({}, {}, {}, {}, {})'.format(self.ingredient_idx, self.name, self.english_name,
                                                       self.description, self.image_url)
