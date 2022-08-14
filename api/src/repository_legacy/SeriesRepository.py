from api.src.data.Series import Series
from api.src.repository_legacy.SQLUtil import SQLUtil


def update_series(series: Series):
    if not isinstance(series, Series):
        raise RuntimeError("update_series(): only allow Series class as parameter")

    set_query = series.get_set_query()

    sql = 'UPDATE series SET {} WHERE series_idx = {}'.format(set_query, series.series_idx)
    print(sql)
    SQLUtil.instance().execute(sql=sql)
