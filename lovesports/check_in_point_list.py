import json

import requests

from config import Config
from utils.console import Console

config = Config()
console = Console()


class CheckInPointList:
    def __init__(self, energy_management):
        self.cookie = {
            "energymanagement": str(energy_management)
        }
        self.url = "http://aitiyuplus.cn:8091/sports-reform/pounchPoints/getCheckInPointList"

    def get(self):
        header = {
            "User-Agent": "okhttp/4.9.3"
        }
        proxy_url = config.get_proxy_url()
        try:
            if proxy_url is not None and proxy_url != "":
                proxy = {"http": proxy_url, "https": proxy_url}
                response = requests.get(url=self.url, cookies=self.cookie, headers=header, proxies=proxy)
            else:
                response = requests.get(url=self.url, cookies=self.cookie, headers=header)
            point_list = json.loads(response.text)["data"]
            region = {}
            for point in point_list:
                p = {
                    "pointName": point["pointName"],
                    "longitude": point["longitude"],
                    "latitude": point["latitude"]
                }
                region.setdefault(point["regionId"], []).append(p)
            return region
        except Exception as e:
            console.error("Get checkpoint list error(Reason: {}).".format(e))
            return None
