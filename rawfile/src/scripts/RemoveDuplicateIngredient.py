from api.src.internal.sql.SqlUtil import SQLUtil


def substitute(ingredient_idx, substitute_ingredient_idx):
    note_query = "SELECT *, type, count(perfume_idx) AS count FROM notes " \
                 "WHERE ingredient_idx = {} OR ingredient_idx = {} " \
                 "GROUP BY perfume_idx " \
        .format(ingredient_idx, substitute_ingredient_idx)
    sql_util = SQLUtil.instance()
    note_list = sql_util.execute(note_query)
    for note in note_list:
        if note['count'] == 1:
            if note['ingredient_idx'] != substitute_ingredient_idx:
                query = "UPDATE notes SET ingredient_idx = {} " \
                        "WHERE ingredient_idx = {} AND perfume_idx = {} AND type = {}" \
                    .format(substitute_ingredient_idx, note['ingredient_idx'], note['perfume_idx'], note['type'])
                sql_util.execute(query)
        elif note['count'] == 2:
            query = "DELETE FROM notes WHERE ingredient_idx = {} AND perfume_idx = {} AND type = {}".format(
                note['ingredient_idx'], note['perfume_idx'], note['type'])
            sql_util.execute(query)
        else:
            raise Exception("???")

    remove_ingredient_query = "DELETE FROM ingredients WHERE ingredient_idx = {}".format(ingredient_idx)
    sql_util.execute(remove_ingredient_query)


def main():
    sql_util = SQLUtil.instance()

    query = "SELECT english_name FROM ingredients GROUP BY english_name HAVING COUNT(english_name) > 1"
    duplicated_english_name_list = sql_util.execute(query)
    for item in duplicated_english_name_list:
        english_name = item['english_name']
        if len(english_name) == 0:
            continue
        query = "SELECT ingredient_idx, name, english_name FROM ingredients WHERE english_name = '{}'".format(
            english_name)
        ingredient_list = sql_util.execute(query)
        idx_list = [item['ingredient_idx'] for item in ingredient_list]
        idx_list.sort()
        correct_idx = idx_list.pop(0)
        for duplicated_idx in idx_list:
            print("{} -> {}".format(duplicated_idx, correct_idx))
            substitute(duplicated_idx, correct_idx)


if __name__ == '__main__':
    main()
