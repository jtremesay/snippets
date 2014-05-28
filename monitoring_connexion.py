#!/usr/bin/env python3
#-*- coding: utf8 -*-

import subprocess
import time


def log(message):
    now_str = time.strftime("%H:%M:%S", time.localtime())
    print("{0} - {1}".format(now_str, message))


def connection_is_up():
    return subprocess.call(("fping", "-q", "8.8.8.8")) == 0


old_is_connected = False
while True:
    new_is_connected = connection_is_up()
    if new_is_connected != old_is_connected:
        if new_is_connected:
            log("connection up")
        else:
            log("connection down")

        old_is_connected = new_is_connected

    time.sleep(1)
