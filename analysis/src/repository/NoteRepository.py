from typing import List

from analysis.src.data.Note import Note
from analysis.src.repository.SQLUtil import SQLUtil


def get_note_list_by_perfume_idx(perfume_idx, note_type) -> List[Note]:
    if note_type:
        sql = 'SELECT perfume_idx, ingredient_idx, type FROM notes WHERE perfume_idx={} AND type={}' \
            .format(perfume_idx, note_type)
    else:
        sql = 'SELECT perfume_idx, ingredient_idx, type FROM notes WHERE perfume_idx={}' \
            .format(perfume_idx)

    SQLUtil.instance().execute(sql=sql)
    return [Note(perfume_idx=it['perfume_idx'], ingredient_idx=it['ingredient_idx'], type=it['type']) for it in
            SQLUtil.instance().fetchall()]


def get_note_list_by_perfume_idx_list(perfume_idx_list) -> List[Note]:
    sql = 'SELECT perfume_idx, ingredient_idx, type FROM notes WHERE perfume_idx in {}' \
        .format("({})".format(", ".join(map(str, perfume_idx_list))))

    SQLUtil.instance().execute(sql=sql)
    return [Note(perfume_idx=it['perfume_idx'], ingredient_idx=it['ingredient_idx'], type=it['type']) for it in
            SQLUtil.instance().fetchall()]


def main():
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../../.env'), verbose=True)

    SQLUtil.instance().logging = True

    result = get_note_list_by_perfume_idx(1, None)
    print(len(result))

    result = get_note_list_by_perfume_idx_list([1, 2, 3])
    print(len(result))


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
