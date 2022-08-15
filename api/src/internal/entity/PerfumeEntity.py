from typing import Optional

from api.src.internal.entity.SqlEntity import SqlEntity


class PerfumeEntity(SqlEntity):
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
