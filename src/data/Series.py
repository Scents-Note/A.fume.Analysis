class Series:

    def __init__(self, series_idx, name, description):
        self.series_idx = series_idx
        self.name = name
        self.description = description

    def __str__(self):
        return 'Series({}, {}, {})'.format(self.series_idx, self.name, self.description)
