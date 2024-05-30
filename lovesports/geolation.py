import json

import requests

from config import Config
from utils.console import Console

config = Config()
console = Console()


class Geolation:
    def __init__(self, geo_id):
        self.id = geo_id
        self.url = "http://aitiyuplus.cn:8091/sports-reform/pounchPoints/findGeolationById?id={}"

    def get(self):
        headers = {
            "Host": "aitiyuplus.cn:8091",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 14; 2211133C Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/121.0.6167.178 Mobile Safari/537.36",
            "X-Requested-With": "com.qdkjd.lovesports",
            "Referer": "http://aitiyuplus:8091/h5/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        proxy_url = config.get_proxy_url()
        try:
            if proxy_url is not None and proxy_url != "":
                proxy = {"http": proxy_url, "https": proxy_url}
                response = requests.get(url=self.url.format(self.id), headers=headers, proxies=proxy)
            else:
                response = requests.get(url=self.url.format(self.id), headers=headers)
            json_response = json.loads(response.text)
            geolations = json_response["data"]["geolations"]
            json_geolations = json.loads(geolations)
            geolation_res = []
            for point in json_geolations["data"]["postionList"]:
                p = {
                    "latitude": point["latitude"],
                    "longitude": point["longitude"]
                }
                geolation_res.append(p)
            return geolation_res
        except Exception as e:
            console.error("Get geolation error(Reason: {})".format(e))
            return None
