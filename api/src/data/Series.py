class Series:

    def __init__(self, idx: int, name: str, description: str, image_url: str):
        self.idx = idx
        self.name = name
        self.description = description
        self.image_url = image_url

    def __str__(self):
        return 'Series({}, {}, {}, {})'.format(self.idx, self.name, self.description, self.image_url)

