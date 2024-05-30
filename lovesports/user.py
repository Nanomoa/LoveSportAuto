import json

import requests

from config import Config
from utils.console import Console

config = Config()
console = Console()


class User:
    def __init__(self, student_id, password):
        self.username = student_id
        self.password = password
        self.url = "http://aitiyuplus.cn:8091/sports-reform/xinhai/login/"

    def login(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
        proxy_url = config.get_proxy_url()
        try:
            if proxy_url is not None and proxy_url != "":
                proxy = {"http": proxy_url, "https": proxy_url}
                response = requests.get(url=self.url + self.username + "/" + self.password,
                                        headers=headers,
                                        proxies=proxy)
            else:
                response = requests.get(url=self.url + self.username + "/" + self.password,
                                        headers=headers)
            user_info = json.loads(response.text)["data"]
            user_info = {
                "name": user_info["name"],
                "id": user_info["id"],
                "token": user_info["token"],
                "energymanagement": response.cookies.get("energymanagement")
            }
            return user_info
        except Exception as e:
            console.error("Login error(Reason: {}).".format(e))
            return None
