import random

import yaml

from utils.console import Console

console = Console()


class Config:
    def __init__(self):
        with open('config.yaml', 'r') as file:
            self.data = yaml.safe_load(file)

    def get_proxy_url(self):
        return self.data['AutoLoveSport']['proxy_url']

    def get_random_region(self):
        regions = self.data['AutoLoveSport']['regions']
        enabled_regions = [region for region in regions if region['enabled'] is True]
        if enabled_regions:
            return random.choice(enabled_regions)
        else:
            return None

    def foreach_users(self, func):
        users = self.data['AutoLoveSport']['users']
        for user in users:
            region_this_user = self.get_random_region()
            if region_this_user:
                success = False
                while not success:
                    success = func(user, region_this_user)
            else:
                console.warning("No region found for user '{}'".format(user['student_id']))
