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


# 長押しされたとみなす時間(秒)
hold_time_sec = 0.5

def main():
    print("Waiting for device to become ready...")
    dev_path = ""
    while(True):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if("B8:27:EB:A2:AE:CE" in device.phys):
                dev_path = device.path
        if (dev_path == "") :
            sleep(1)
        else : break

    dev = InputDevice(dev_path)
    dev_name = dev.name
    dev_phys = dev.phys

    print("IoT Button is ready.")
    old = 0
    button_android = 0
    button_ios = 0

    for event in dev.read_loop():

        if event.type == ecodes.EV_KEY:

            print("------------調査用-------------")
            print("type:" + str(event.type))
            print("value" + str(event.value))
            print("code" + str(event.code))
            print(evdev.ecodes.KEY[115])
            print("-------------------------------")

            if event.value == 1: #キーを押し下げる
                if event.code == evdev.ecodes.KEY_VOLUMEUP:  #キーコード：115。なぜかどちらのボタンをクリックしてもkey:115が飛ぶ
                    button_android = 1
                    button_ios = 1
                    push_time = time() #押した時間の記録

            if event.value == 0: #キーを押し上げる

                if time() - push_time > hold_time_sec: #長押しのとき
                    ConnectServer(dev_name,dev_phys,"button hold")
                else:
                    ConnectServer(dev_name,dev_phys,"button push")


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