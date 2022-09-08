from api.src.internal.entity.PerfumeEntity import PerfumeEntity
from api.src.internal.sql.SqlModel import SqlModel
from api.src.internal.sql.SqlUtil import SQLUtil


def main(perfume_idx_list):
    fail_list = []
    for perfume_idx in perfume_idx_list:
        image_url = "https://afume-release.s3.ap-northeast-2.amazonaws.com/perfumes/{}_1.png".format(perfume_idx)
        perfume = PerfumeEntity(perfume_idx=perfume_idx, name=None, english_name=None, story=None, volume_and_price=None,
                                abundance_rate=None, image_url=image_url)
        affected_rows = SqlModel.instance().update(perfume)
        if affected_rows == 0:
            fail_list.append(perfume_idx)
    print("faile list : {}".format(fail_list))


if __name__ == '__main__':
    sql_util = SQLUtil.instance()
    sql_util.logging = True
    main([])
