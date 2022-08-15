class Perfume:
    abundance_rate_list = ['', '코롱', '오 드 코롱', '오 드 뚜왈렛', '오 드 퍼퓸', '퍼퓸', '기타']

    def __init__(self, idx: int, name: str, english_name: str, image_url: str, story: str, volume_and_price: str,
                 abundance_rate: int):
        self.idx = idx
        self.name = name
        self.english_name = english_name
        self.image_url = image_url
        self.story = story
        self.volume_and_price = volume_and_price
        self.abundance_rate = abundance_rate

    def __str__(self):
        return 'Perfume({}, {}, {}, {})'.format(self.idx, self.name, self.english_name, self.image_url)
