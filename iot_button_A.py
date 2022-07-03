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
    dev_name = dev.name
    dev_phys = dev.phys

    print("IoT Button is ready.")
    old = 0
    iOS_flag=0
    is_android = 0

    for event in dev.read_loop():

        if event.type == ecodes.EV_KEY:

            print("type:" + str(event.type))
            print("value" + str(event.value))
            print("code" + str(event.code))

            if event.value == 1:
                if event.code == 115:  # when android button pushed
                    is_android=1

            # key upが始まったら
            if event.value == 0:
                if iOS_flag==1 :
                    iOS_flag=0
                    continue

                # 長押し終わり
                if old != 0 and time() - old > hold_time_sec:
                    if is_android :
                        ConnectServer(dev_name,dev_phys,"Android hold")
                        is_android=0
                        iOS_flag=1
                    else:
                        ConnectServer(dev_name,dev_phys,"iOS hold")

                    old = 0
                    continue
                if is_android:
                    ConnectServer(dev_name,dev_phys,"Android push")
                    is_android=0
                    iOS_flag=1
                else:
                    ConnectServer(dev_name,dev_phys,"iOS push")

            # 長押しスタート
            if event.value == 2 and old == 0:
                old = time()


def ConnectServer(dev_name,dev_phys,button):
        try:
                url = 'https://script.google.com/macros/s/AKfycbyUGtXrzmUod2y_3eNAeyBJKS6bRWd0eX3FtW-STDVJY24vbhS1iWEXyuP47rAqp2An0A/exec'+'?device_name='+dev_name+'&device_phys='+dev_phys+'&button='+button
                print(button)
                requests.get(url)

        except error.HTTPError as err:
                print(err.code)
        except error.URLError as err:
                print(err.reason)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
print("\n")