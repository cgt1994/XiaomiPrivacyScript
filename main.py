# This is a sample Python script.
import os
import subprocess
import commands
import re


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# def set_info_value(self, value):
#     self.info_value = value


# 只能获取执行结果
def getoutput(stmt):
    return subprocess.getoutput(stmt)
    # 执行失败不需要特殊处理，因为该方法无法判断失败成功，只负责将结果进行返回
    # 返回执行结果，但是结果返回的是一个str字符串（不论有多少行）


class DevicePrivacyInfo:

    def __init__(self, name, command, pattern=None):
        self.info_name = name
        self.info_value = set()
        self.command = command
        self.init(pattern)

    def init(self, pattern):
        if pattern is None:
            self.set_value(getoutput(self.command))
        else:
            self.set_value(re.findall(pattern, getoutput(self.command)))

    def print_detail(self):
        print(f"[info_name : {self.info_name}, info_value : {self.info_value}]")

    def set_value(self, value):
        # print(f"set_value,value == {value},type == {type(value)}")
        if isinstance(value, str):
            self.info_value.add(value)
        elif isinstance(value, list) and len(list(value)) != 0:
            for element in value:
                self.set_value(element)
        elif isinstance(value, tuple) and len(tuple(value)) != 0:
            for element in value:
                self.set_value(element)


def print_line():
    print("----------")


def exit(msg):
    print(msg)
    raise SystemExit(0)


def check_devices_connect():
    result = getoutput('adb devices')
    print_line()
    device_list = re.findall(r"(.+?)	device", result)
    if len(device_list) < 1:
        exit("No devices found, please connect devices first")
    else:
        print('Device founded == ' + device_list[0])


device_info = set()


def add_device_config():
    device_info.add(DevicePrivacyInfo("SN", "adb get-serialno"))
    device_info.add(DevicePrivacyInfo("longitude and latitude",
                                      "adb shell dumpsys location | grep 'last location=Location\\[network'",
                                      r"last location=Location\[network (.+?),(.+?) \S"))
    device_info.add(DevicePrivacyInfo("Android ID", "adb shell settings get secure android_id"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # first, check at least one device connected
    check_devices_connect()

    # init devices config
    add_device_config()
    for device in device_info:
        device.print_detail()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
