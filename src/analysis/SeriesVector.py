import pandas as pd

from src.data.Note import Note
from src.repository import PerfumeRepository, NoteRepository, IngredientRepository, SeriesRepository

PERFUME_IDX = 'perfume_idx'
PERFUME_NAME = '향수 이름'
SERIES_IDX = 'series_idx'
INGREDIENT_IDX = 'ingredient_idx'


def get_series_vector():
    perfume_list = PerfumeRepository.get_all_perfume()
    perfume_map = {
        p.idx: p
        for p in perfume_list
    }

    note_list = NoteRepository.get_note_list_by_perfume_idx_list(perfume_map.keys())
    ingredient_list = IngredientRepository.get_ingredient_list([note.ingredient_idx for note in note_list])
    ingredient_map = {
        ingredient.idx: ingredient
        for ingredient in ingredient_list
    }
    series_list = SeriesRepository.get_series_all()
    series_map = {
        series.idx: series
        for series in series_list
    }

    note_df = pd.DataFrame(map(Note.get_json, note_list))

    note_df.insert(0, SERIES_IDX,
                   [int(ingredient_map.get(ingredient_idx).series_idx) for ingredient_idx in
                    note_df[INGREDIENT_IDX]], True)

    series_name_list = [s.name for s in series_list]

    series_vector_df = pd.DataFrame([], columns=[PERFUME_IDX, PERFUME_NAME] + series_name_list)
    for perfume_idx, group_data in note_df.groupby(PERFUME_IDX):
        series_counter = group_data.groupby(SERIES_IDX).size()
        total = sum(series_counter.values)

        def normalize(x):
            return float(x) / total

        series_dic = {
            series.name: normalize(series_counter[series.idx]) if series.idx in series_counter else 0
            for series in series_list
        }

        series_dic[PERFUME_IDX] = perfume_idx
        series_dic[PERFUME_NAME] = perfume_map[perfume_idx].name

        series_vector_df = series_vector_df.append(series_dic, ignore_index=True)

    return series_vector_df


def main():
    df = get_series_vector()
    df.to_excel(
        "output.xlsx"
    )


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    main()
