import hashlib
import json
import random
import socket
import time
from collections import OrderedDict

import geopy.distance
from alive_progress import alive_bar

from utils.console import Console

console = Console()


class DataTemplate:
    def __init__(self, student_id, app_device, userid):
        self.submit_num = 0
        self.punch_points = []
        self.geolations = []
        self.total_distance = 0
        self.offset_second = 0
        self.processbar = None

        self.json_data = {}
        self.json_data["startDatetime"] = self.get_time()
        self.json_data["subMit"] = str(self.submit_num + 1)
        self.json_data["punchPoints"] = self.get_punch_points()
        self.json_data["addVersion"] = "1.3.9"
        self.json_data["summile"] = self.get_summile()
        self.json_data["appDevice"] = app_device
        self.json_data["userid"] = userid
        self.json_data["dateFlag"] = self.get_date_flag()
        self.json_data["avgSpeed"] = self.get_avg_speed()
        self.json_data["geolations"] = self.get_geolations()
        self.json_data["unqualified"] = 0
        self.json_data["total"] = self.get_total()
        self.json_data["stepNumber"] = self.get_step_number()
        self.json_data["userType"] = "student"
        self.json_data["id"] = str(student_id) + "-" + str(self.json_data["startDatetime"])
        self.json_data["updatetime"] = 0
        self.json_data["pointNum"] = len(self.punch_points)
        self.json_data["endDatetime"] = 0
        self.json_data["key"] = self.get_key()
        self._SportId = self.json_data["id"]

    def refresh_json(self):
        self.json_data["subMit"] = str(self.submit_num)
        self.json_data["punchPoints"] = self.get_punch_points()
        self.json_data["summile"] = self.get_summile()
        self.json_data["dateFlag"] = self.get_date_flag()
        self.json_data["avgSpeed"] = self.get_avg_speed()
        self.json_data["geolations"] = self.get_geolations()
        self.json_data["unqualified"] = 0
        self.json_data["total"] = self.get_total()
        self.json_data["stepNumber"] = self.get_step_number()
        self.json_data["updatetime"] = 0
        self.json_data["pointNum"] = len(self.punch_points)
        self.json_data["endDatetime"] = self.get_time()
        self.json_data["key"] = self.get_key()

    def get_time(self):
        return int(time.time() * 10 ** 3 + self.offset_second * 10 ** 3)

    def get_summile(self):
        return str(round(self.total_distance / 1000, 2))

    def set_submit_num(self, num):
        self.submit_num = num

    def get_submit_num(self):
        return self.submit_num

    def add_punch_points(self, new_punch_points):
        last_data = new_punch_points
        new_punch_points = OrderedDict()
        new_punch_points["lng"] = last_data["longitude"]
        new_punch_points["t"] = self.get_time()
        new_punch_points["lat"] = last_data["latitude"]
        if len(self.punch_points) == 0:
            self.punch_points = [new_punch_points]
        else:
            self.punch_points.append(new_punch_points)

    def get_punch_points(self):
        json_str = json.dumps(self.punch_points, ensure_ascii=False)
        return str(json_str)

    def add_geolation(self, new_geolations):
        new_geolations["t"] = self.get_time()
        last_data = new_geolations
        new_geolations = OrderedDict()
        new_geolations["t"] = last_data["t"]
        new_geolations["latitude"] = last_data["latitude"]
        new_geolations["longitude"] = last_data["longitude"]

        if len(self.geolations) == 0:
            self.geolations = [new_geolations]

        else:
            self.geolations.append(new_geolations)
            pre_location = (self.geolations[-2]["latitude"], self.geolations[-2]["longitude"])
            next_location = (self.geolations[-1]["latitude"], self.geolations[-1]["longitude"])
            self.add_distance(geopy.distance.geodesic(pre_location, next_location).m)

    def add_distance(self, distance):
        self.total_distance += distance

    def get_date_flag(self):
        seconds = int((self.get_time() - self.json_data["startDatetime"]) / 1000)
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        formatted_time = "{:d}'{:02d}''".format(minutes, remaining_seconds)
        return formatted_time

    def get_avg_speed(self):
        if self.total_distance == 0:
            return "0'00'"
        seconds = int((self.get_time() - self.json_data["startDatetime"]) / 1000)
        speed = int(seconds / (self.total_distance / 1000))
        minutes = speed // 60
        remaining_seconds = speed % 60
        formatted_speed = "{:d}'{:02d}''".format(minutes, remaining_seconds)
        return formatted_speed

    def get_geolations(self):
        geo_data = {
            "code": 200,
            "data": {
                "postionList": self.geolations,
            },
            "success": True
        }
        geo_data_str = json.dumps(geo_data, ensure_ascii=False)
        geo_data_str = geo_data_str.replace(" ", "")
        return geo_data_str

    def get_total(self):
        return int(self.total_distance)

    @staticmethod
    def get_md5(content):
        if not content:
            return ""
        md5_hash = hashlib.md5()
        md5_hash.update(content.encode('utf-8'))
        return md5_hash.hexdigest()

    def get_md5_iterations(self, ori_str, iterations):
        if not ori_str:
            return ""
        for _ in range(iterations):
            ori_str = self.get_md5(ori_str)
        return ori_str

    def get_step_number(self):
        return int(self.total_distance * 1.2 + random.randint(0, 10))

    def get_key(self):
        geolations_str = self.get_geolations()
        a = int(len(geolations_str) / 2)
        geolations_str = geolations_str[0:a]
        return self.get_md5_iterations(self.json_data["id"] + geolations_str, 1)

    def get_json(self):
        self.refresh_json()
        json_str = json.dumps(self.json_data, ensure_ascii=False)
        json_str = json_str.replace(" ", "")
        return json_str


class Running(DataTemplate):
    def __init__(self, student_id, app_device, userid, energymanagement, checkpoints, geolation_list, region_id):
        super().__init__(student_id=student_id, app_device=app_device, userid=userid)
        self.student_id = student_id
        self.app_device = app_device
        self.userid = userid
        self.energymanagement = energymanagement
        self.checkpoints = checkpoints
        self.geolation_list = geolation_list
        self.region_id = region_id
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def post_data(self, data):
        headers = """\
POST /sports-reform/pounchPoints/addGeolation/add HTTP/1.1
Content-Type: application/json; charset=UTF-8
Content-Length: 794
Host: aitiyuplus.cn:8091
Connection: Keep-Alive
Accept-Encoding: gzip
Cookie: energymanagement=94349681-55f0-4f32-bf62-6bec9d5b9161
User-Agent: okhttp/4.9.3\r\n\r\n"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        content_length = len(data)
        headers = headers.replace("Content-Length: 794", f"Content-Length: {content_length}")
        headers = headers.replace("Cookie: energymanagement=94349681-55f0-4f32-bf62-6bec9d5b9161",
                                  "Cookie: energymanagement={}".format(self.energymanagement))
        request = headers + data
        host = "aitiyuplus.cn"
        port = 8091
        response = ""
        if self.submit_num == 0:
            for i in range(300):
                try:
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client_socket.settimeout(10)
                    self.client_socket.connect((host, port))
                    self.client_socket.send(request.encode())
                    response = self.client_socket.recv(4096000)
                    break
                except socket.timeout:
                    console.error(
                        "Connection timed out during result submission, retrying for {}th time.".format(i + 1))
                except socket.error as e:
                    console.error(
                        "Connection error during result submission(Reason: {}), retrying for {}th time.".format(e,
                                                                                                                i + 1))
                except:
                    console.error(
                        "An unknown error occurred during result submission, in the {}th retry.".format(i + 1))
        else:
            for i in range(3):
                try:
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client_socket.settimeout(10)
                    self.client_socket.connect((host, port))
                    self.client_socket.send(request.encode())
                    response = self.client_socket.recv(4096000)
                    break
                except socket.timeout:
                    console.error(
                        "Connection timed out during checkpoint submission, retrying for {}th time.".format(i + 1))
                except socket.error as e:
                    console.error(
                        "Connection error during checkpoint submission(Reason: {}), retrying for {}th time.".format(e,
                                                                                                                    i + 1))
                except:
                    console.error(
                        "An unknown error occurred during checkpoint submission, in the {}th retry.".format(i + 1))
        if response != "":
            # print(response.decode("utf-8"))
            return response.decode("utf-8")
        else:
            console.error("Submission of the {}th punch point failed and has been skipped".format(self.submit_num))
            return response

    def upload(self, last=False):
        if last:
            self.set_submit_num(self.get_submit_num())
        else:
            self.set_submit_num(self.get_submit_num() + 1)
        self.submit_num = self.get_submit_num()
        upload_data = self.get_json()
        upload_data = json.loads(upload_data)
        time.sleep(0.1)
        upload_data["updatetime"] = self.get_time()
        if last:
            upload_data["subMit"] = "0"
            self.submit_num = 0
        upload_data = json.dumps(upload_data, ensure_ascii=False)
        upload_data = upload_data.replace(" ", "")
        self.post_data(upload_data)

    def get_region_checkpoints(self):
        return self.checkpoints[self.region_id]

    def get_checkpoints_this_time(self):
        region_checkpoints = self.get_region_checkpoints()
        checkpoints = region_checkpoints + region_checkpoints
        mark = {i: False for i in range(len(checkpoints))}
        checkpoints_res = []
        for geo_item in self.geolation_list:
            for i in range(len(checkpoints)):
                distance = geopy.distance.geodesic(
                    (geo_item["latitude"], geo_item["longitude"]),
                    (checkpoints[i]["latitude"], checkpoints[i]["longitude"])
                ).m
                if distance < 20 and not mark[i]:
                    mark[i] = True
                    checkpoints_res.append(
                        {
                            "latitude": checkpoints[i]["latitude"],
                            "longitude": checkpoints[i]["longitude"]
                        }
                    )
                elif distance >= 20 and mark[i]:
                    mark[i] = False
        result = [checkpoints_res[0]]
        pre_checkpoint = checkpoints_res[0]
        for checkpoint in checkpoints_res[1:]:
            if checkpoint != pre_checkpoint:
                result.append(checkpoint)
                pre_checkpoint = checkpoint
        return result[0:4]

    def start(self):
        console.info("Student {} starts running.".format(self.student_id))
        checkpoints = self.get_checkpoints_this_time()
        mark = {i: False for i in range(len(checkpoints))}
        cnt_checkpoint = 0
        index = 0
        next_checkpoint = checkpoints[index]
        is_punch_completed = False
        with alive_bar(len(self.geolation_list), title="Student {}:".format(self.student_id), force_tty=True) as bar:
            for position in self.geolation_list:
                self.add_geolation(position)
                if cnt_checkpoint >= 4:
                    if not is_punch_completed:
                        is_punch_completed = True
                        console.success(
                            "The punch list for student {}'s run has been completed.".format(self.student_id))
                else:
                    distance = geopy.distance.geodesic(
                        (position["latitude"], position["longitude"]),
                        (next_checkpoint["latitude"], next_checkpoint["longitude"])
                    ).m
                    if distance < 20 and not mark[index] and index <= 3:
                        self.add_punch_points(next_checkpoint)
                        self.upload()
                        console.info("Student {} arrives at the punching point ({},{}).".format(
                            self.student_id, next_checkpoint["latitude"], next_checkpoint["longitude"]
                        ))
                        mark[index] = True
                        cnt_checkpoint += 1
                        if index < 3:
                            index += 1
                            next_checkpoint = checkpoints[index]
                time.sleep(2)
                bar()
        self.upload(last=True)
        console.success("Student {} finished this run.".format(self.student_id))
        console.info("Pace: {}, Mileage: {}.".format(
            self.get_avg_speed(),
            self.get_total()
        ))
