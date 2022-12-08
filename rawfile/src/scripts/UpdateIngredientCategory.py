from api.src.internal.sql.SqlUtil import SQLUtil


def main(category_list):
    sql_util = SQLUtil.instance()

    insert_sql_list = []
    for category in category_list:
        query = "SELECT COUNT(*) as A FROM ingredient_categories " \
                "WHERE name = %s "
        result = sql_util.execute(query, [category])[0]
        if result["A"] == 0:
            insert_sql_list.append("INSERT INTO ingredient_categories(name) VALUES('{}')".format(category))
    print(insert_sql_list)
    if not sql_util.debug:
        for sql in insert_sql_list:
            sql_util.execute(sql)


if __name__ == '__main__':
    main([])
