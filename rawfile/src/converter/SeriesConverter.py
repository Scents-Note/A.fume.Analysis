from api.src.Config import Config
from api.src.internal.entity.SeriesEntity import SeriesEntity
from api.src.internal.sql.SqlModel import series_model
from rawfile.src.common.util.ExcelParser import ExcelColumn, ExcelParser
from rawfile.src.converter.Converter import Converter


class SeriesConverter(Converter):

    def __init__(self):
        super().__init__("{}_series_raw".format(Config.instance().MYSQL_DB))
        self.parser = None

    def get_data_list(self):
        return [
            {
                ExcelColumn.COL_IDX: it.series_idx,
                ExcelColumn.COL_NAME: it.name,
                ExcelColumn.COL_ENGLISH_NAME: it.english_name,
                ExcelColumn.COL_DESCRIPTION: it.description,
                ExcelColumn.COL_IMAGE_URL: it.image_url
            }
            for it in series_model.read_all()
        ]

    def prepare_parser(self, columns_list):
        self.parser = ExcelParser(columns_list, {
            'series_idx': ExcelColumn.COL_IDX,
            'name': ExcelColumn.COL_NAME,
            'english_name': ExcelColumn.COL_ENGLISH_NAME,
            'image_url': ExcelColumn.COL_IMAGE_URL,
            'description': ExcelColumn.COL_DESCRIPTION
        }, lambda it: SeriesEntity.create(it))

    def read_line(self, row):
        series = self.parser.parse(row)
        series_model.update(series.__dict__)
