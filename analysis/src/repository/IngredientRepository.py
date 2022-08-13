from typing import List

from analysis.src.data.Ingredient import Ingredient
from analysis.src.repository.SQLUtil import SQLUtil


def get_ingredient_list(ingredient_idx_list) -> List[Ingredient]:
    sql = 'SELECT * FROM ingredients WHERE ingredient_idx in {}' \
        .format("({})".format(", ".join(map(str, ingredient_idx_list))))

    SQLUtil.instance().execute(sql=sql)
    return [Ingredient(idx=it['ingredient_idx'], series_idx=it['series_idx'], name=it['name'],
                       english_name=it['english_name'], description=it['description'], image_url=it['image_url'])
            for it in SQLUtil.instance().fetchall()]


def main():
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../../.env'), verbose=True)

    SQLUtil.instance().logging = True

    result = get_ingredient_list([1, 2, 3, 4, 5])
    print(len(result))


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
