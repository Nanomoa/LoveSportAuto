import math
import random


class RandomOffset:
    def __init__(self, latitude, longitude):
        self.position = {
            "latitude": latitude,
            "longitude": longitude
        }

    def get(self):
        earth_radius = 6371000.0
        offset_distance = random.uniform(-0.5, 0.5)
        delta_lat = offset_distance / earth_radius * (180 / math.pi)
        latitude_rad = math.radians(self.position["latitude"])
        delta_lon = offset_distance / (earth_radius * math.cos(latitude_rad)) * (180 / math.pi)
        offset_latitude = random.choice([-1, 1]) * delta_lat
        offset_longitude = random.choice([-1, 1]) * delta_lon
        return {
            "latitude": round(self.position["latitude"] + offset_latitude, 6),
            "longitude": round(self.position["longitude"] + offset_longitude, 6)
        }
