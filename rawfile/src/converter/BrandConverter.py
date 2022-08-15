from api.src.Config import Config
from api.src.entity.SqlEntity import Brand
from api.src.repository.CrudRepository import CrudRepository
from api.src.sql.SQLUtil import SQLUtil
from rawfile.src.common.util.ExcelParser import ExcelColumn, ExcelParser
from rawfile.src.converter.Converter import Converter


class BrandConverter(Converter):

    def __init__(self):
        super().__init__("{}_brands_raw".format(Config.instance().MYSQL_DB))
        self.parser = None

    def get_data_list(self):
        SQLUtil.instance().execute(
            sql="SELECT brand_idx AS '{}', name AS '{}', english_name AS '{}', first_initial AS '{}', image_url"
                " AS '{}', description AS {} FROM brands"
                .format(ExcelColumn.COL_IDX, ExcelColumn.COL_NAME, ExcelColumn.COL_ENGLISH_NAME,
                        ExcelColumn.COL_FIRST_INITIAL, ExcelColumn.COL_IMAGE_URL, ExcelColumn.COL_DESCRIPTION))

        return SQLUtil.instance().fetchall()

    def prepare_parser(self, columns_list):
        self.parser = ExcelParser(columns_list=columns_list, column_dict={
            'idx': ExcelColumn.COL_IDX,
            'name': ExcelColumn.COL_NAME,
            'english_name': ExcelColumn.COL_ENGLISH_NAME,
            'first_initial': ExcelColumn.COL_FIRST_INITIAL,
            'description': ExcelColumn.COL_DESCRIPTION,
            'image_url': ExcelColumn.COL_IMAGE_URL
        }, doTask=lambda json: Brand(brand_idx=json['idx'], name=json['name'], english_name=json['english_name'],
                                     first_initial=json['first_initial'],
                                     description=json['description'], image_url=json['image_url']))

    def read_line(self, row: any):
        brand = self.parser.parse(row)
        CrudRepository.update(brand)
