from api.src.Config import Config
from api.src.internal.entity.BrandEntity import BrandEntity
from api.src.internal.sql.SqlModel import brand_model
from rawfile.src.common.util.ExcelParser import ExcelColumn, ExcelParser
from rawfile.src.converter.Converter import Converter


class BrandConverter(Converter):

    def __init__(self):
        super().__init__("{}_brands_raw".format(Config.instance().MYSQL_DB))
        self.parser = None

    def get_data_list(self):
        return [{
            ExcelColumn.COL_IDX: brand.brand_idx,
            ExcelColumn.COL_NAME: brand.name,
            ExcelColumn.COL_FIRST_INITIAL: brand.first_initial,
            ExcelColumn.COL_IMAGE_URL: brand.image_url,
            ExcelColumn.COL_DESCRIPTION: brand.description
        } for brand in brand_model.read_all()]

    def prepare_parser(self, columns_list):
        self.parser = ExcelParser(columns_list=columns_list, column_dict={
            'brand_idx': ExcelColumn.COL_IDX,
            'name': ExcelColumn.COL_NAME,
            'first_initial': ExcelColumn.COL_FIRST_INITIAL,
            'description': ExcelColumn.COL_DESCRIPTION,
            'image_url': ExcelColumn.COL_IMAGE_URL
        }, doTask=lambda data: BrandEntity.create(data))

    def read_line(self, row: any):
        brand = self.parser.parse(row)
        brand_model.update(brand.__dict__)
