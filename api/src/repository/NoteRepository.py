from typing import List

from api.src.data.Note import Note
from api.src.internal.sql.SqlModel import note_model
from api.src.internal.sql.SqlUtil import SQLUtil

sql_util = SQLUtil.instance()


class NoteRepository:

    @staticmethod
    def get_note_list_by_perfume_idx(perfume_idx, note_type) -> List[Note]:
        sql = 'SELECT perfume_idx, ingredient_idx, type FROM notes WHERE perfume_idx={} AND type={}' \
            .format(perfume_idx, note_type)
        result = sql_util.execute(sql=sql)
        if result is None:
            return []
        return [Note(perfume_idx=it['perfume_idx'], ingredient_idx=it['ingredient_idx'], note_type=it['type']) for it in
                result]

    @staticmethod
    def update_note_list(perfume_idx, note_type, update_list):
        for note in update_list:
            if note.perfume_idx != perfume_idx or note.type != note_type:
                raise RuntimeError("Logic Error")

        db_list = NoteRepository.get_note_list_by_perfume_idx(perfume_idx=perfume_idx, note_type=note_type)
        note_set = set(update_list)
        db_set = set(db_list)

        intersection_set = note_set.intersection(db_set)
        note_set = note_set - intersection_set
        db_set = db_set - intersection_set

        added_set = note_set.difference(db_set)
        removed_set = db_set.difference(note_set)

        [note_model.create(note.__dict__) for note in added_set]
        [note_model.delete(note.__dict__) for note in removed_set]

    @staticmethod
    def get_note_list_by_perfume_idx_and_note(perfume_idx: int, note_type: int = None) -> List[Note]:
        if note_type:
            sql = 'SELECT perfume_idx, ingredient_idx, type FROM notes WHERE perfume_idx={} AND type={}' \
                .format(perfume_idx, note_type)
        else:
            sql = 'SELECT perfume_idx, ingredient_idx, type FROM notes WHERE perfume_idx={}' \
                .format(perfume_idx)

        result = sql_util.execute(sql=sql)
        return [Note(perfume_idx=it['perfume_idx'], ingredient_idx=it['ingredient_idx'], note_type=it['type']) for it in
                result]

    @staticmethod
    def get_note_list_by_perfume_idx_list(perfume_idx_list) -> List[Note]:
        sql = 'SELECT perfume_idx, ingredient_idx, type FROM notes WHERE perfume_idx in {}' \
            .format("({})".format(", ".join(map(str, perfume_idx_list))))

        result = sql_util.execute(sql=sql)
        return [Note(perfume_idx=it['perfume_idx'], ingredient_idx=it['ingredient_idx'], note_type=it['type']) for it in
                result]
