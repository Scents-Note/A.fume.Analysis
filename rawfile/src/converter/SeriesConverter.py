from api.src.Config import Config
from api.src.internal.entity.SeriesEntity import SeriesEntity
from api.src.internal.entity.SqlModel import series_model
from api.src.internal.sql.SQLUtil import SQLUtil
from rawfile.src.common.util.ExcelParser import ExcelColumn, ExcelParser
from rawfile.src.converter.Converter import Converter


class SeriesConverter(Converter):

    def __init__(self):
        super().__init__("{}_series_raw".format(Config.instance().MYSQL_DB))
        self.parser = None

    def get_data_list(self):
        SQLUtil.instance().execute(
            sql="SELECT s.series_idx AS {}, s.name AS {}, s.english_name AS {}, s.description AS {}, "
                "s.image_url AS {} FROM series AS s"
            .format(ExcelColumn.COL_IDX, ExcelColumn.COL_NAME, ExcelColumn.COL_ENGLISH_NAME,
                    ExcelColumn.COL_DESCRIPTION, ExcelColumn.COL_IMAGE_URL))

        return SQLUtil.instance().fetchall()

    def prepare_parser(self, columns_list):
        self.parser = ExcelParser(columns_list, {
            'series_idx': ExcelColumn.COL_IDX,
            'name': ExcelColumn.COL_NAME,
            'english_name': ExcelColumn.COL_ENGLISH_NAME,
            'image_url': ExcelColumn.COL_IMAGE_URL,
            'description': ExcelColumn.COL_DESCRIPTION
        }, lambda result_json: SeriesEntity(series_idx=result_json['series_idx'], name=result_json['name'],
                                            english_name=result_json['english_name'],
                                            image_url=result_json['image_url'],
                                            description=result_json['description']))

    def read_line(self, row):
        series = self.parser.parse(row)
        series_model.update(series.__dict__)
