class Series:

    def __init__(self, idx, name, description):
        self.idx = idx
        self.name = name
        self.description = description

    def __str__(self):
        return 'Series({}, {}, {})'.format(self.idx, self.name, self.description)
