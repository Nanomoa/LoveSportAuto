import json
import random


class GeolationId:
    def __init__(self, region_id):
        self.region_id = region_id
        file_path = './geolation-data.json'
        # 打开json文件并读取其内容
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def get(self):
        if self.data is not None and len(self.data) > 0:
            region_geolation_id_list = self.data[self.region_id]
            if len(region_geolation_id_list) > 0:
                return region_geolation_id_list[random.randint(0, len(region_geolation_id_list) - 1)]
            else:
                return None
        else:
            return None
