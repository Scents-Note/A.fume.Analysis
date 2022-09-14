from typing import List

from api.src.data.Ingredient import Ingredient, IngredientInfo
from api.src.internal.sql.SqlUtil import SQLUtil

sql_util = SQLUtil.instance()


class IngredientRepository:

    @staticmethod
    def get_ingredient_idx_by_name(name: str) -> int:
        sql = 'SELECT ingredient_idx FROM ingredients WHERE name="{}" OR english_name="{}"'.format(name, name)
        result = sql_util.open(
            sql_util.executeCommand(sql=sql),
            sql_util.fetchallCommand()
        )[0]
        if result is None:
            raise RuntimeError("Wrong Ingredient name:[{}]".format(name))
        return result[0]['ingredient_idx']

    @staticmethod
    def get_category_idx_by_name(name: str):
        sql = 'SELECT id FROM ingredient_categories WHERE name="{}"'.format(name)
        result = sql_util.execute(sql=sql)
        if len(result) == 0:
            raise RuntimeError("Wrong IngredientCategory name:[{}]".format(name))
        return result[0]['id']

    @staticmethod
    def get_ingredient_list(ingredient_idx_list: [int]) -> List[Ingredient]:
        sql = 'SELECT * FROM ingredients WHERE ingredient_idx in {}' \
            .format("({})".format(", ".join(map(str, ingredient_idx_list))))
        result = sql_util.execute(sql=sql)
        return [Ingredient(idx=it['ingredient_idx'], series_idx=it['series_idx'], name=it['name'],
                           description=it['description'],
                           image_url=it['image_url'])
                for it in result]

    @staticmethod
    def get_ingredient_info_list() -> List[IngredientInfo]:

        result = sql_util.execute(
            sql="SELECT i.ingredient_idx as idx, i.name, i.english_name, "
                "i.description, i.image_url, i.series_idx, s.name AS series_name,"
                " i.category_idx, ic.name as category_name "
                " FROM ingredients i "
                " INNER JOIN series s ON s.series_idx = i.series_idx "
                " LEFT JOIN ingredient_categories ic ON ic.id = i.category_idx "
                " ORDER BY i.ingredient_idx")
        return [IngredientInfo.create(row) for row in result]


def main():
    sql_util.logging = True
    sql_util.debug = True

    result = IngredientRepository.get_ingredient_list([1, 2, 3, 4, 5])
    print(len(result))


if __name__ == '__main__':
    main()
