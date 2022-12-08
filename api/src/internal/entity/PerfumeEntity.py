from typing import Optional


class PerfumeEntity:
    abundance_rate_list = ['', '코롱', '오 드 코롱', '오 드 뚜왈렛', '오 드 퍼퓸', '퍼퓸', '기타']

    def __init__(self, perfume_idx: int, name: Optional[str] = None, english_name: Optional[str] = None,
                 brand_idx: Optional[int] = None,
                 image_url: Optional[str] = None,
                 story: Optional[str] = None, volume_and_price: Optional[str] = None,
                 abundance_rate: Optional[int] = None,
                 deleted_at: Optional[str] = None):
        self.perfume_idx = perfume_idx
        self.name = name
        self.english_name = english_name
        self.brand_idx = brand_idx
        self.image_url = image_url
        self.story = story
        self.volume_and_price = volume_and_price
        self.abundance_rate = abundance_rate
        self.deleted_at = deleted_at
