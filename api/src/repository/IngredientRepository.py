from typing import List

from api.src.data.Ingredient import Ingredient, IngredientInfo
from api.src.internal.sql.SQLUtil import SQLUtil


class IngredientRepository:

    @staticmethod
    def get_ingredient_idx_by_name(name):
        sql = 'SELECT ingredient_idx FROM ingredients WHERE name="{}"'.format(name)
        SQLUtil.instance().execute(sql=sql)
        result = SQLUtil.instance().fetchall()
        if len(result) == 0:
            raise RuntimeError("Wrong Ingredient name:[{}]".format(name))
        return result[0]['ingredient_idx']

    @staticmethod
    def get_category_idx_by_name(name: str):
        sql = 'SELECT id FROM ingredient_categories WHERE name="{}"'.format(name)
        SQLUtil.instance().execute(sql=sql)
        result = SQLUtil.instance().fetchall()
        if len(result) == 0:
            raise RuntimeError("Wrong IngredientCategory name:[{}]".format(name))
        return result[0]['id']

    @staticmethod
    def carate_ingredient_category(name):
        sql = 'INSERT ingredient_categories(name) VALUES({})'.format(name)
        print(sql)
        SQLUtil.instance().execute(sql=sql)

    @staticmethod
    def get_ingredient_list(ingredient_idx_list: [int]) -> List[Ingredient]:
        sql = 'SELECT * FROM ingredients WHERE ingredient_idx in {}' \
            .format("({})".format(", ".join(map(str, ingredient_idx_list))))

        SQLUtil.instance().execute(sql=sql)
        return [Ingredient(idx=it['ingredient_idx'], series_idx=it['series_idx'], name=it['name'],
                           description=it['description'],
                           image_url=it['image_url'])
                for it in SQLUtil.instance().fetchall()]

    @staticmethod
    def get_ingredient_info_list() -> List[IngredientInfo]:

        SQLUtil.instance().execute(
            sql="SELECT i.ingredient_idx as idx, i.name, i.english_name, "
                "i.description, i.image_url, i.series_idx, s.name AS series_name,"
                " i.category_idx, ic.name as category_name "
                " FROM ingredients i "
                " INNER JOIN series s ON s.series_idx = i.series_idx "
                " LEFT JOIN ingredient_categories ic ON ic.id = i.category_idx "
                " ORDER BY i.ingredient_idx")
        return [IngredientInfo.create(row) for row in SQLUtil.instance().fetchall()]


def main():
    SQLUtil.instance().logging = True

    result = IngredientRepository.get_ingredient_list([1, 2, 3, 4, 5])
    print(len(result))


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
