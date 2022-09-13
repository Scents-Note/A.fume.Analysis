class NoteEntity:
    TYPE_TOP = 1
    TYPE_MIDDLE = 2
    TYPE_BASE = 3
    TYPE_SINGLE = 4

    def __init__(self, perfume_idx: int, ingredient_idx: int, note_type: int):
        self.perfume_idx = perfume_idx
        self.ingredient_idx = ingredient_idx
        self.type = note_type
