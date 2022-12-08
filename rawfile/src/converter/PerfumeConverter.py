import datetime

from api.src.Config import Config
from api.src.internal.entity.NoteEntity import NoteEntity
from api.src.internal.entity.PerfumeEntity import PerfumeEntity
from api.src.internal.sql.SqlModel import perfume_model
from api.src.repository.BrandRepository import BrandRepository
from api.src.repository.IngredientRepository import IngredientRepository
from api.src.repository.NoteRepository import NoteRepository
from api.src.internal.sql.SqlUtil import SQLUtil
from rawfile.src.common.util.ExcelParser import ExcelColumn, ExcelParser
from rawfile.src.converter.Converter import Converter

wrong_ingredient_name_list = []


class PerfumeConverter(Converter):
    def __init__(self):
        super().__init__("{}_perfumes_raw".format(Config.instance().MYSQL_DB))
        self.perfume_parser = None
        self.default_review_parser = None
        self.note_parser = None

    def get_data_list(self):
        sql_util = SQLUtil.instance()
        perfume_list = sql_util.execute(sql='SELECT p.perfume_idx AS {}, '.format(ExcelColumn.COL_IDX) +
                                            'p.name AS {},'.format(ExcelColumn.COL_NAME) +
                                            'p.english_name AS {},'.format(ExcelColumn.COL_ENGLISH_NAME) +
                                            'b.name AS {},'.format(ExcelColumn.COL_BRAND) +
                                            'p.image_url AS {},'.format(ExcelColumn.COL_MAIN_IMAGE) +

                                            'p.story AS {},'.format(ExcelColumn.COL_STORY) +
                                            'p.volume_and_price AS {},'.format(ExcelColumn.COL_VOLUME_AND_PRICE) +
                                            'p.abundance_rate AS {},'.format(ExcelColumn.COL_ABUNDANCE_RATE) +
                                            'IF(p.deleted_at IS NULL, \'O\', \'X\') AS {}, '.format(
                                                ExcelColumn.COL_PUBLIC) +

                                            '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                            'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                            'p.perfume_idx AND n.`type` = 1 ) AS {},'.format(ExcelColumn.COL_TOP_NOTE) +

                                            '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                            'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                            'p.perfume_idx AND n.`type` = 2 ) AS {},'.format(
                                                ExcelColumn.COL_MIDDLE_NOTE) +

                                            '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                            'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                            'p.perfume_idx AND n.`type` = 3 ) AS {},'.format(
                                                ExcelColumn.COL_BASE_NOTE) +

                                            '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                            'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                            'p.perfume_idx AND n.`type` = 4 ) AS {},'.format(
                                                ExcelColumn.COL_SINGLE_NOTE) +

                                            '" " AS `[국내 출시]` '

                                            'FROM perfumes AS p '
                                            'INNER JOIN brands AS b '
                                            'ON p.brand_idx = b.brand_idx '
                                            'GROUP BY p.perfume_idx '
                                            'ORDER BY p.perfume_idx')

        for perfume in perfume_list:
            perfume[ExcelColumn.COL_ABUNDANCE_RATE] = PerfumeEntity.abundance_rate_list[
                perfume[ExcelColumn.COL_ABUNDANCE_RATE]]

        return perfume_list

    def prepare_parser(self, columns_list):

        def doTaskPerfume(json) -> PerfumeEntity:
            def convert(text: str) -> str:
                if text == "퍼퓸드 오일" or text == "센티드 워터" or text == "오 프라체":
                    return "기타"
                if text == "코롱" or text == "샤워 코롱" or text == "오드 코롱":
                    return "오 드 코롱"
                if text == "엑스뜨레 드 퍼퓸" or text == "퍼퓸 드 엑스뜨레":
                    return "퍼퓸"
                return text.strip()

            abundance_rate = PerfumeEntity.abundance_rate_list.index(
                convert(json['abundance_rate_str'])) if json['abundance_rate_str'] is not None else None
            if abundance_rate == -1:
                raise RuntimeError("abundance_rate_str is not invalid: " + json['abundance_rate_str'])
            deleted_at = 'NULL' if json['public'] == 'O' else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            json['deleted_at'] = deleted_at if json['public'] is not None else None

            brand_idx = BrandRepository.getBrandIdx(json['brand_name']) if json['brand_name'] is not None else None

            return PerfumeEntity(perfume_idx=json['perfume_idx'], name=json['name'], english_name=json['english_name'],
                                 brand_idx=brand_idx,
                                 image_url=json['image_url'], story=json['story'],
                                 volume_and_price=json['volume_and_price'], abundance_rate=abundance_rate,
                                 deleted_at=json['deleted_at'])

        def doTaskNoteList(json) -> dict:
            perfume_idx = json['perfume_idx']

            def parse_note_str(note_str: str, note_type: int) -> [NoteEntity]:
                if note_str is None:
                    return None

                note_list = []
                ingredient_list = [it.strip() for it in note_str.split(',')]

                for ingredient_name in ingredient_list:
                    try:
                        ingredient_idx = IngredientRepository.get_ingredient_idx_by_name(ingredient_name)
                        note_list.append(
                            NoteEntity(perfume_idx=perfume_idx, ingredient_idx=ingredient_idx, note_type=note_type))
                    except RuntimeError as err:
                        print(err)
                        wrong_ingredient_name_list.append(ingredient_name)

                return note_list

            ret = {NoteEntity.TYPE_TOP: parse_note_str(json['top_note_str'], NoteEntity.TYPE_TOP),
                   NoteEntity.TYPE_MIDDLE: parse_note_str(json['middle_note_str'], NoteEntity.TYPE_MIDDLE),
                   NoteEntity.TYPE_BASE: parse_note_str(json['base_note_str'], NoteEntity.TYPE_BASE),
                   NoteEntity.TYPE_SINGLE: parse_note_str(json['single_note_str'], NoteEntity.TYPE_SINGLE)}
            return ret

        self.perfume_parser = ExcelParser(columns_list, {
            'perfume_idx': ExcelColumn.COL_IDX,
            'name': ExcelColumn.COL_NAME,
            'brand_name': ExcelColumn.COL_BRAND,
            'english_name': ExcelColumn.COL_ENGLISH_NAME,
            'image_url': ExcelColumn.COL_MAIN_IMAGE,
            'story': ExcelColumn.COL_STORY,
            'volume_and_price': ExcelColumn.COL_VOLUME_AND_PRICE,
            'abundance_rate_str': ExcelColumn.COL_ABUNDANCE_RATE,
            'public': ExcelColumn.COL_PUBLIC
        }, doTaskPerfume)

        self.note_parser = ExcelParser(columns_list, {
            'perfume_idx': ExcelColumn.COL_IDX,
            'top_note_str': ExcelColumn.COL_TOP_NOTE,
            'middle_note_str': ExcelColumn.COL_MIDDLE_NOTE,
            'base_note_str': ExcelColumn.COL_BASE_NOTE,
            'single_note_str': ExcelColumn.COL_SINGLE_NOTE
        }, doTaskNoteList)

        IngredientRepository.init_cache()
        print(wrong_ingredient_name_list)

    def read_line(self, row):
        perfume = self.perfume_parser.parse(row)
        print("-------{}----------".format(perfume.perfume_idx))
        if perfume.perfume_idx is None:
            if perfume.image_url is None:
                perfume.image_url = ""
            if perfume.volume_and_price is None:
                perfume.volume_and_price = ""
            if perfume.story is None:
                perfume.story = ""
            perfume_model.create(perfume.__dict__)
        else:
            perfume_model.update(perfume.__dict__)
            note_dict = self.note_parser.parse(row)
            for note_type, note_list in note_dict.items():
                if note_list is None:
                    continue
                NoteRepository.update_note_list(perfume_idx=perfume.perfume_idx, update_list=note_list,
                                                note_type=note_type)
