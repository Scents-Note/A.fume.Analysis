from api.src.internal.sql.SqlUtil import SQLUtil

sql_util = SQLUtil.instance()

cache_dict_ingredient_by_name = {}
cache_dict_category_by_name = {}


class BrandRepository:

    @staticmethod
    def getBrandIdx(brand_name: str):
        sql = 'SELECT brand_idx FROM brands WHERE name=%s'
        sql_util.logging = True
        result = sql_util.execute(sql=sql, args=[brand_name])
        print(result)
        if len(result) == 0:
            raise RuntimeError("Wrong Brand name:[{}]".format(brand_name))
        return result[0]['brand_idx']


if __name__ == '__main__':
    print(BrandRepository.getBrandIdx("겔랑"))