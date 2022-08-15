from api.src.Config import Config
from api.src.internal.entity.IngredientEntity import IngredientEntity
from api.src.internal.entity.SqlModel import ingredient_model
from api.src.repository.IngredientRepository import IngredientRepository
from api.src.internal.sql.SQLUtil import SQLUtil
from rawfile.src.common.util.ExcelParser import ExcelColumn, ExcelParser
from rawfile.src.converter.Converter import Converter


class IngredientConverter(Converter):

    def __init__(self):
        super().__init__("{}_ingredients_raw".format(Config.instance().MYSQL_DB))
        self.parser = None

    def get_data_list(self):
        SQLUtil.instance().execute(
            sql="SELECT i.ingredient_idx AS {}, i.name AS {}, i.english_name AS {}, "
                "i.description AS {}, i.image_url AS {}, i.series_idx AS {}, s.name AS `[{}]`,"
                " ic.name as {} "
                " FROM ingredients i "
                " INNER JOIN series s ON s.series_idx = i.series_idx "
                " LEFT JOIN ingredient_categories ic ON ic.id = i.category_idx "
                " ORDER BY i.ingredient_idx"
            .format(ExcelColumn.COL_IDX, ExcelColumn.COL_NAME, ExcelColumn.COL_ENGLISH_NAME,
                    ExcelColumn.COL_DESCRIPTION, ExcelColumn.COL_IMAGE_URL,
                    ExcelColumn.COL_SERIES_IDX, ExcelColumn.COL_SERIES_NAME, ExcelColumn.COL_CATEGORY))

        return SQLUtil.instance().fetchall()

    def prepare_parser(self, columns_list):
        self.parser = ExcelParser(columns_list=columns_list, column_dict={
            'idx': ExcelColumn.COL_IDX,
            'name': ExcelColumn.COL_NAME,
            'english_name': ExcelColumn.COL_ENGLISH_NAME,
            'description': ExcelColumn.COL_DESCRIPTION,
            'image_url': ExcelColumn.COL_IMAGE_URL,
            'series_idx': ExcelColumn.COL_SERIES_IDX,
            'category': ExcelColumn.COL_CATEGORY
        }, doTask=lambda json: IngredientEntity(ingredient_idx=json['idx'], name=json['name'],
                                                english_name=json['english_name'],
                                                description=json['description'],
                                                image_url=json['image_url'],
                                                series_idx=json['series_idx'],
                                                category_idx=IngredientRepository.get_category_idx_by_name(
                                                    json['category'])))

    def read_line(self, row):
        ingredient = self.parser.parse(row)
        ingredient_model.update(ingredient.__dict__)
