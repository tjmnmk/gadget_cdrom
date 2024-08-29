# -*- coding:utf-8 -*-

MODE_CD = "cd"
MODE_HDD = "hdd"
MODE_USB = "usb"
MODE_SHUTDOWN = "shutdown"
MODE_UPLOAD = "web-upload"

ALL_MODES = [MODE_CD, MODE_HDD, MODE_USB, MODE_SHUTDOWN, MODE_UPLOAD]
BROWSE_MODES = [MODE_CD, MODE_USB]

FILE_EXTS = {
    MODE_CD: "iso",
    MODE_USB: "img",
}