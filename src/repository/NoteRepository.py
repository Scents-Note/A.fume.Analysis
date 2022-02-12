from src.data.Note import Note
from src.repository.SQLUtil import SQLUtil


def get_note_list_by_perfume_idx(perfume_idx, note_type):
    if note_type:
        sql = 'SELECT perfume_idx, ingredient_idx, type FROM notes WHERE perfume_idx={} AND type={}' \
            .format(perfume_idx, note_type)
    else:
        sql = 'SELECT perfume_idx, ingredient_idx, type FROM notes WHERE perfume_idx={}' \
            .format(perfume_idx)

    SQLUtil.instance().execute(sql=sql)
    return [Note(perfume_idx=it['perfume_idx'], ingredient_idx=it['ingredient_idx'], type=it['type']) for it in
            SQLUtil.instance().fetchall()]


def main():
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    SQLUtil.instance().logging = True

    result = get_note_list_by_perfume_idx(1, None)

    for x in result:
        print(x)


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
