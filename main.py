from config import Config
from lovesports.check_in_point_list import CheckInPointList
from lovesports.geolation import Geolation
from lovesports.running import Running
from lovesports.user import User
from utils.console import Console
from utils.geolation_id import GeolationId
from utils.random_offset import RandomOffset

console = Console()
config = Config()


def start_application():
    print("""\
 █████╗ ██╗   ██╗████████╗ ██████╗     ██╗      ██████╗ ██╗   ██╗███████╗    ███████╗██████╗  ██████╗ ██████╗ ████████╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗    ██║     ██╔═══██╗██║   ██║██╔════╝    ██╔════╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
███████║██║   ██║   ██║   ██║   ██║    ██║     ██║   ██║██║   ██║█████╗      ███████╗██████╔╝██║   ██║██████╔╝   ██║
██╔══██║██║   ██║   ██║   ██║   ██║    ██║     ██║   ██║╚██╗ ██╔╝██╔══╝      ╚════██║██╔═══╝ ██║   ██║██╔══██╗   ██║
██║  ██║╚██████╔╝   ██║   ╚██████╔╝    ███████╗╚██████╔╝ ╚████╔╝ ███████╗    ███████║██║     ╚██████╔╝██║  ██║   ██║
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝     ╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝    ╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝
    """)
    console.success("Service startup.")


def start_running(info: {}, region: {}):
    # 用户登陆
    user_info = User(info["student_id"], info["password"]).login()
    if user_info is not None:
        console.success("Student {} logged in successfully.".format(info["student_id"]))
    else:
        console.write_line("Service suspension.")
        return False
    # 获取打卡点列表
    check_in_point_list = CheckInPointList(user_info["energymanagement"]).get()
    if check_in_point_list is not None:
        console.success("Get checkpoints success.")
    else:
        console.write_line("Service suspension.")
        return False
    # 获取本次跑步的路径id
    geo_id = GeolationId(region['id']).get()
    if geo_id is None:
        console.error("Get geolation id failed.")
        console.write_line("Service suspension.")
        return False
    # 获取本次跑步的路径坐标
    geolations = Geolation(geo_id).get()
    if geolations is not None:
        console.success("Get geolation success.")
    else:
        console.write_line("Service suspension.")
        return False
    console.info("The venue of this run is: {}".format(region['title']))
    # 随机化偏移路径坐标
    geolation_list = []
    for point in geolations:
        point_offset = RandomOffset(point["latitude"], point["longitude"]).get()
        geolation_list.append(point_offset)
    # 开始跑步
    Running(
        student_id=info["student_id"],
        app_device=info["app_device"],
        userid=user_info["id"],
        energymanagement=user_info["energymanagement"],
        checkpoints=check_in_point_list,
        geolation_list=geolation_list,
        region_id=region["id"]
    ).start()
    return True


def main():
    start_application()
    config.foreach_users(start_running)


if __name__ == "__main__":
    main()
