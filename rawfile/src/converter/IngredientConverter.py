from api.src.Config import Config
from api.src.internal.entity.IngredientEntity import IngredientEntity
from api.src.internal.sql.SqlModel import ingredient_model
from api.src.repository.IngredientRepository import IngredientRepository
from api.src.repository.SeriesRepository import SeriesRepository
from rawfile.src.common.util.ExcelParser import ExcelColumn, ExcelParser
from rawfile.src.converter.Converter import Converter


class IngredientConverter(Converter):

    def __init__(self):
        super().__init__("{}_ingredients_raw".format(Config.instance().MYSQL_DB))
        self.parser = None

    def get_data_list(self):
        return [
            {ExcelColumn.COL_IDX: it.idx,
             ExcelColumn.COL_NAME: it.name,
             ExcelColumn.COL_ENGLISH_NAME: it.english_name,
             ExcelColumn.COL_DESCRIPTION: it.description,
             ExcelColumn.COL_IMAGE_URL: it.image_url,
             ExcelColumn.COL_SERIES_NAME: it.series_name,
             ExcelColumn.COL_CATEGORY: it.category_name
             }
            for it in IngredientRepository.get_ingredient_info_list()
        ]

    def prepare_parser(self, columns_list):
        def doTask(data: dict):
            data['category_idx'] = IngredientRepository.get_category_idx_by_name(
                data['category']) if data['category'] is not None else None
            data.pop('category')
            data['series_idx'] = SeriesRepository.get_series_idx(data['series_name']) \
                if data['series_name'] is not None else None
            data.pop('series_name')
            return IngredientEntity.create(data)

        self.parser = ExcelParser(columns_list=columns_list, column_dict={
            'ingredient_idx': ExcelColumn.COL_IDX,
            'name': ExcelColumn.COL_NAME,
            'english_name': ExcelColumn.COL_ENGLISH_NAME,
            'description': ExcelColumn.COL_DESCRIPTION,
            'image_url': ExcelColumn.COL_IMAGE_URL,
            'series_name': ExcelColumn.COL_SERIES_NAME,
            'category': ExcelColumn.COL_CATEGORY
        }, doTask=doTask)

    def read_line(self, row):
        ingredient = self.parser.parse(row)
        if ingredient.ingredient_idx is None:
            if ingredient.description is None:
                ingredient.description = ""
            if ingredient.image_url is None:
                ingredient.image_url = ""
            ingredient_model.create(ingredient.__dict__)
        else:
            ingredient_model.update(ingredient.__dict__)
