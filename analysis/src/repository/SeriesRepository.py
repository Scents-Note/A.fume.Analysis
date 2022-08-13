from typing import List

from analysis.src.data.Series import Series
from analysis.src.repository.SQLUtil import SQLUtil


def get_series_all() -> List[Series]:
    sql = 'SELECT * FROM series'

    SQLUtil.instance().execute(sql=sql)
    return [Series(idx=it['series_idx'], name=it['name'], description=it['description'])
            for it in SQLUtil.instance().fetchall()]


def main():
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../../.env'), verbose=True)

    SQLUtil.instance().logging = True

    result = get_series_all()
    print(len(result))


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
