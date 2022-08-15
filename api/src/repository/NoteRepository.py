from analysis.src.repository.SQLUtil import SQLUtil
from api.src.entity.SqlEntity import Note
from api.src.repository.CrudRepository import CrudRepository


class NoteRepository:

    @staticmethod
    def get_note_list_by_perfume_idx(perfume_idx, note_type):
        sql = 'SELECT perfume_idx, ingredient_idx, type FROM notes WHERE perfume_idx={} AND type={}' \
            .format(perfume_idx, note_type)
        SQLUtil.instance().execute(sql=sql)
        return [Note(perfume_idx=it['perfume_idx'], ingredient_idx=it['ingredient_idx'], note_type=it['type']) for it in
                SQLUtil.instance().fetchall()]

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

        [CrudRepository.create(note) for note in added_set]
        [CrudRepository.delete(note) for note in removed_set]

