import abc
from typing import Optional


class SqlEntity(abc.ABC):

    @abc.abstractmethod
    def get_primary_keys(self) -> [str]:
        pass

    @abc.abstractmethod
    def get_table_name(self) -> str:
        pass

    def get_ids(self) -> [int]:
        return [self.__dict__[pk] for pk in self.get_primary_keys()]

    def generate_update_condition(self) -> (str, [any]):
        dic = self.__dict__
        keys = filter(lambda key: key not in self.get_primary_keys() and dic[key] is not None, dic.keys())
        condition_str = ', '.join(['{} = {}'.format(key, '%d' if dic[key].isnumeric() else '%s') for key in keys])
        value_list = [dic[key] for key in keys]
        return condition_str, value_list

    def generate_primary_key_condition(self) -> (str, [any]):
        dic = self.__dict__
        keys = self.get_primary_keys()
        condition_str = ', '.join(['{} = {}'.format(pk, '%d') for pk in keys])
        value_list = [dic[key] for key in keys]
        return condition_str, value_list


class Brand(SqlEntity):

    def __init__(self, brand_idx: int, name: str, english_name: str, first_initial: str, description: str,
                 image_url: str):
        self.brand_idx = brand_idx
        self.name = name
        self.english_name = english_name
        self.first_initial = first_initial
        self.description = description
        self.image_url = image_url

    def get_table_name(self) -> str:
        return 'brands'

    def get_primary_keys(self) -> [str]:
        return ['brand_idx']


class Ingredient(SqlEntity):

    def __init__(self, ingredient_idx: int, name: str, english_name: str, description: str, image_url: str,
                 series_idx: int, category_idx: int):
        self.ingredient_idx = ingredient_idx
        self.name = name
        self.english_name = english_name
        self.description = description
        self.image_url = image_url
        self.series_idx = series_idx
        self.category_idx = category_idx

    def get_primary_keys(self) -> [str]:
        return ['brand_idx']

    def get_table_name(self) -> str:
        return 'ingredients'


class IngredientCategory(SqlEntity):

    def __init__(self, id: int, name: str, used_count_on_perfume: int):
        self.id = id
        self.name = name
        self.used_count_on_perfume = used_count_on_perfume

    def get_primary_keys(self) -> [str]:
        return ['id']

    def get_table_name(self) -> str:
        return 'ingredient_categories'


class Series(SqlEntity):

    def __init__(self, series_idx: int, name: str, english_name: str, description: str, image_url: str):
        self.series_idx = series_idx
        self.name = name
        self.english_name = english_name
        self.description = description
        self.image_url = image_url

    def get_primary_keys(self) -> [str]:
        return ['series_idx']

    def get_table_name(self) -> str:
        return 'series'


class Note(SqlEntity):
    TYPE_TOP = 1
    TYPE_MIDDLE = 2
    TYPE_BASE = 3
    TYPE_SINGLE = 4

    def __init__(self, perfume_idx: int, ingredient_idx: int, note_type: int):
        self.perfume_idx = perfume_idx
        self.ingredient_idx = ingredient_idx
        self.note_type = note_type

    def get_primary_keys(self) -> [str]:
        return ['perfume_idx', 'ingredient_idx']

    def get_table_name(self) -> str:
        return 'notes'


class Perfume(SqlEntity):
    abundance_rate_list = ['', '코롱', '오 드 코롱', '오 드 뚜왈렛', '오 드 퍼퓸', '퍼퓸', '기타']

    def __init__(self, idx: int, name: Optional[str] = None, english_name: Optional[str] = None,
                 image_url: Optional[str] = None,
                 story: Optional[str] = None, volume_and_price: Optional[str] = None,
                 abundance_rate: Optional[int] = None):
        self.idx = idx
        self.name = name
        self.english_name = english_name
        self.image_url = image_url
        self.story = story
        self.volume_and_price = volume_and_price
        self.abundance_rate = abundance_rate

    def get_primary_keys(self) -> [str]:
        return ['perfume_idx']

    def get_table_name(self) -> str:
        return 'perfumes'
