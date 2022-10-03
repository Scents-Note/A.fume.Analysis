class NoteEntity:
    TYPE_TOP = 1
    TYPE_MIDDLE = 2
    TYPE_BASE = 3
    TYPE_SINGLE = 4

    def __init__(self, perfume_idx: int, ingredient_idx: int, note_type: int):
        self.perfume_idx = perfume_idx
        self.ingredient_idx = ingredient_idx
        self.type = note_type

    def __hash__(self):
        return self.perfume_idx * 100 + self.ingredient_idx * 10 + self.type

    def __eq__(self, other):
        if not isinstance(self, NoteEntity):
            return False
        return self.perfume_idx == other.perfume_idx and self.ingredient_idx == other.ingredient_idx and self.type == other.type
