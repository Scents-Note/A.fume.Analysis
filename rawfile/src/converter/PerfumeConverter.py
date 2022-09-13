from api.src.Config import Config
from api.src.internal.entity.NoteEntity import NoteEntity
from api.src.internal.entity.PerfumeEntity import PerfumeEntity
from api.src.internal.sql.SqlModel import perfume_model
from api.src.repository.IngredientRepository import IngredientRepository
from api.src.repository.NoteRepository import NoteRepository
from api.src.internal.sql.SqlUtil import SQLUtil
from rawfile.src.common.util.ExcelParser import ExcelColumn, ExcelParser
from rawfile.src.converter.Converter import Converter


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

                             '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                             'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                             'p.perfume_idx AND n.`type` = 1 ) AS {},'.format(ExcelColumn.COL_TOP_NOTE) +

                             '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                             'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                             'p.perfume_idx AND n.`type` = 2 ) AS {},'.format(ExcelColumn.COL_MIDDLE_NOTE) +

                             '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                             'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                             'p.perfume_idx AND n.`type` = 3 ) AS {},'.format(ExcelColumn.COL_BASE_NOTE) +

                             '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                             'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                             'p.perfume_idx AND n.`type` = 4 ) AS {},'.format(ExcelColumn.COL_SINGLE_NOTE) +

                             # 'AVG(r.score) AS `[평균점수]`, '
                             # '(SELECT COUNT(lp.user_idx) FROM like_perfumes AS lp WHERE '
                             # 'lp.perfume_idx = p.perfume_idx) AS `[좋아요]`, '

                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx) '
                             # 'AS `[리뷰개수]`, '
                             #
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND seasonal = 0) AS `[계절감_평가X]`, '
                             #
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND seasonal = 1) AS `[봄]` ,'
                             #
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND seasonal = 2) AS `[여름]`, '
                             #
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND seasonal = 3) AS `[가을]`, '
                             #
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND seasonal = 4) AS `[겨울]`, '
                             #
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND sillage = 0) AS `[잔향감_평가X]`, '
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND sillage = 1) AS `[잔향감_가벼움]`, '
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND sillage = 2) AS `[잔향감_보통]`, '
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND sillage = 3) AS `[잔향감_무거움]`, '

                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND longevity = 0) AS `[지속감_평가X]`, '
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND longevity = 1) AS `[지속감_매우_약함]`, '
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND longevity = 2) AS `[지속감_약함]`, '
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND longevity = 3) AS `[지속감_보통]`, '
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND longevity = 4) AS `[지속감_강함]`, '
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND longevity = 5) AS `[지속감_매우_강함]`, '

                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND gender = 1) AS `[성별감_남성]`, '
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND gender = 2) AS `[성별감_중성]`, '
                             # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                             # 'AND gender = 3) AS `[성별감_여성]`, '

                             # '(SELECT GROUP_CONCAT(k.name) FROM keywords AS k INNER JOIN '
                             # 'join_perfume_keywords AS jpk ON k.id = jpk.perfume_idx '
                             # 'WHERE jpk.perfume_idx = p.perfume_idx) AS `[키워드]`,'

                             '" " AS `[국내 출시]` '

                             'FROM perfumes AS p '
                             'INNER JOIN brands AS b '
                             'ON p.brand_idx = b.brand_idx '
                             # 'LEFT JOIN reviews AS r '
                             # 'ON p.perfume_idx = r.perfume_idx '
                             'GROUP BY p.perfume_idx')

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
                return text

            abundance_rate = PerfumeEntity.abundance_rate_list.index(
                convert(json['abundance_rate_str'])) if json['abundance_rate_str'] is not None else None
            if abundance_rate == -1:
                raise RuntimeError("abundance_rate_str is not invalid: " + json['abundance_rate_str'])
            return PerfumeEntity(perfume_idx=json['perfume_idx'], name=json['name'], english_name=json['english_name'],
                                 image_url=json['image_url'], story=json['story'],
                                 volume_and_price=json['volume_and_price'], abundance_rate=abundance_rate)

        def doTaskNoteList(json) -> dict:
            perfume_idx = json['perfume_idx']

            def parse_note_str(note_str: str, note_type: int) -> [NoteEntity]:
                if note_str is None:
                    return None

                note_list = []
                ingredient_list = [it.strip() for it in note_str.split(',')]

                for ingredient_name in ingredient_list:
                    ingredient_idx = IngredientRepository.get_ingredient_idx_by_name(ingredient_name)
                    note_list.append(
                        NoteEntity(perfume_idx=perfume_idx, ingredient_idx=ingredient_idx, note_type=note_type))

                return note_list

            ret = {NoteEntity.TYPE_TOP: parse_note_str(json['top_note_str'], NoteEntity.TYPE_TOP),
                   NoteEntity.TYPE_MIDDLE: parse_note_str(json['middle_note_str'], NoteEntity.TYPE_MIDDLE),
                   NoteEntity.TYPE_BASE: parse_note_str(json['base_note_str'], NoteEntity.TYPE_BASE),
                   NoteEntity.TYPE_SINGLE: parse_note_str(json['single_note_str'], NoteEntity.TYPE_SINGLE)}
            return ret

        self.perfume_parser = ExcelParser(columns_list, {
            'perfume_idx': ExcelColumn.COL_IDX,
            'name': ExcelColumn.COL_NAME,
            'english_name': ExcelColumn.COL_ENGLISH_NAME,
            'image_url': ExcelColumn.COL_MAIN_IMAGE,
            'story': ExcelColumn.COL_STORY,
            'volume_and_price': ExcelColumn.COL_VOLUME_AND_PRICE,
            'abundance_rate_str': ExcelColumn.COL_ABUNDANCE_RATE
        }, doTaskPerfume)

        self.note_parser = ExcelParser(columns_list, {
            'perfume_idx': ExcelColumn.COL_IDX,
            'top_note_str': ExcelColumn.COL_TOP_NOTE,
            'middle_note_str': ExcelColumn.COL_MIDDLE_NOTE,
            'base_note_str': ExcelColumn.COL_BASE_NOTE,
            'single_note_str': ExcelColumn.COL_SINGLE_NOTE
        }, doTaskNoteList)

    def read_line(self, row):
        perfume = self.perfume_parser.parse(row)
        perfume_model.update(perfume.__dict__)

        note_dict = self.note_parser.parse(row)
        for note_type, note_list in note_dict.items():
            if note_list is None:
                continue
            NoteRepository.update_note_list(perfume_idx=perfume.perfume_idx, update_list=note_list, note_type=note_type)
