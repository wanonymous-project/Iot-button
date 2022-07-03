
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python IoT Button"""


import evdev
from evdev import InputDevice, categorize, ecodes
import datetime
from time import time, sleep
from urllib import request, error
import requests
#import settings


# ホールドされたとみなす時間(秒)
hold_time_sec = 0.5


def main():
    print("Waiting for device to become ready...")
    dev_path = ""
    while(True):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if("Shutter" in device.name):
                dev_path = device.path
        if (dev_path == "") :
            sleep(1)
        else : break

    dev = InputDevice(dev_path)
    print("IoT Button is ready.")
    old = 0
    iOS_flag=0
    is_android = 0
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.value == 1:
                if event.code == 28:  # when android button pushed
                    is_android=1

            # key upが始まったら
            if event.value == 0:
                if iOS_flag==1 :