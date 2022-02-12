class Note:
    TYPE_TOP = 1
    TYPE_MIDDLE = 2
    TYPE_BASE = 3
    TYPE_SINGLE = 4

    def __init__(self, perfume_idx, ingredient_idx, type):
        self.perfume_idx = perfume_idx
        self.ingredient_idx = ingredient_idx
        self.type = type

    def __str__(self):
        return 'Note({}, {}, {})'.format(self.perfume_idx, self.ingredient_idx, self.type)
