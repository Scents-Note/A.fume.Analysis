from api.src.data.Perfume import Perfume
from api.src.repository_legacy.SQLUtil import SQLUtil


def update_perfume(perfume):
    if not isinstance(perfume, Perfume):
        raise RuntimeError("update_perfume(): only allow Perfume class as parameter")

    perfume_idx = perfume.idx
    json = perfume.get_json()
    if json is None:
        return
    json.pop('idx')
    set_condition = ', '.join(['{} = %s'.format(it) for it in json.keys()])
    values = [str(json[it]) for it in json.keys()]

    sql = 'UPDATE perfumes SET {} WHERE perfume_idx = {}'.format(set_condition, perfume_idx)
    SQLUtil.instance().execute(sql=sql, args=values)


def main():
    SQLUtil.instance().logging = True

    testPerfume = Perfume(idx=1, name='154 코롱 조말론 런던',
                          english_name='154 Cologne Jo Malone London for women and men', image_url=None)
    update_perfume(testPerfume)


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()

