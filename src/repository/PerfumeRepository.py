from typing import List

from src.data.Perfume import Perfume
from src.repository.SQLUtil import SQLUtil


def get_all_perfume() -> List[Perfume]:
    sql = 'SELECT * from perfumes'

    SQLUtil.instance().execute(sql=sql)
    return [Perfume(idx=it['perfume_idx'], name=it['name'], english_name=it['english_name'], image_url=it['image_url'])
            for it in SQLUtil.instance().fetchall()]


def main():
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    SQLUtil.instance().logging = True

    print(get_all_perfume())


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
