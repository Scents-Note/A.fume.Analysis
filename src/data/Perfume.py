
class Perfume:
    def __init__(self, idx, name, english_name, image_url):
        self.idx = idx
        self.name = name
        self.english_name = english_name
        self.image_url = image_url

    def get_json(self):
        json = {'idx': self.idx}
        if self.name is not None:
            json['name'] = self.name
        if self.english_name is not None:
            json['english_name'] = self.english_name
        if self.image_url is not None:
            json['image_url'] = self.image_url
        if len(json.keys()) == 1:
            return
        return json

    def __str__(self):
        return 'Perfume({}, {}, {}, {})'.format(self.idx, self.name, self.english_name, self.image_url)
