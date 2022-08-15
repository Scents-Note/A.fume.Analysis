from api.src.internal.entity.SqlEntity import SqlEntity


class IngredientCategoryEntity(SqlEntity):

    def __init__(self, idx: int, name: str, used_count_on_perfume: int):
        self.idx = idx
        self.name = name
        self.used_count_on_perfume = used_count_on_perfume

    def get_primary_keys(self) -> [str]:
        return ['id']

    def get_table_name(self) -> str:
        return 'ingredient_categories'
