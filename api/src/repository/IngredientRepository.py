from typing import List

from analysis.src.repository.SQLUtil import SQLUtil
from api.src.data.Ingredient import Ingredient


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
    def get_category_idx_by_name(name):
        sql = 'SELECT idx FROM ingredient_categories WHERE name="{}"'.format(name)
        SQLUtil.instance().execute(sql=sql)
        result = SQLUtil.instance().fetchall()
        if len(result) == 0:
            raise RuntimeError("Wrong IngredientCategory name:[{}]".format(name))
        return result[0]['idx']

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
                           english_name=it['english_name'], description=it['description'],
                           image_url=it['image_url'])
                for it in SQLUtil.instance().fetchall()]


def main():
    SQLUtil.instance().logging = True

    result = IngredientRepository.get_ingredient_list([1, 2, 3, 4, 5])
    print(len(result))


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
