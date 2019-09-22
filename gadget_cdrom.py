#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time
import traceback
import random
import subprocess
import spidev
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
APP_DIR = os.path.dirname(os.path.realpath(__file__))

MODE_CD = "cd"
MODE_HDD = "hdd"


class SH1106:
    def __init__(self):
        spi = spidev.SpiDev(0, 0)
        spi.max_speed_hz = 2000000
        spi.mode = 0
        self._spi = spi

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RESET_PIN, GPIO.OUT)
        GPIO.setup(self.DC_PIN, GPIO.OUT)
        GPIO.setup(self.CS_PIN, GPIO.OUT)
        GPIO.setup(self.BL_PIN, GPIO.OUT)

        GPIO.output(self.CS_PIN, 0)
        GPIO.output(self.BL_PIN, 1)
        GPIO.output(self.DC_PIN, 0)

        self.reset()
        self._run_commands(self.INIT_COMMANDS)
        time.sleep(0.1)
        self._run_command(0xAF)

    def _run_command(self, command):
        GPIO.output(self.DC_PIN, GPIO.LOW)
        self._spi.writebytes((command,))

    def _run_commands(self, commands):
        for command in commands:
            self._run_command(command)

    def reset(self):
        GPIO.output(self.RESET_PIN, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(self.RESET_PIN, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.RESET_PIN, GPIO.HIGH)
        time.sleep(0.1)

    def display_image(self, pil_image, invert = True):
        buf_size = self.HEIGHT_RES * self.WIDTH_RES // 8
        buf = [0xFF] * buf_size
        image_raw_pixels = pil_image.convert('1').load()
        for y in range(self.HEIGHT_RES):
            for x in range(self.WIDTH_RES):
                if image_raw_pixels[x, y] == 0:
                    buf[x + (y // 8) * self.WIDTH_RES] &= ~(1 << (y % 8))

        for page in range(0, self.HEIGHT_RES // 8):
            self._run_command(0xB0 + page)
            self._run_command(0x02)
            self._run_command(0x10)
            time.sleep(0.01)
            GPIO.output(self.DC_PIN, GPIO.HIGH)

            for i in range(0, self.WIDTH_RES):
                page_data = buf[i + self.WIDTH_RES * page]
                if not invert:
                    page_data = ~page_data
                self._spi.writebytes((~page_data,))

    HEIGHT_RES = 64
    WIDTH_RES = 128
    RESET_PIN       = 25
    DC_PIN          = 24
    CS_PIN          = 8
    BL_PIN          = 18
    INIT_COMMANDS   = (0xAE,
    0x02,
    0x10,
    0x40,
    0x81,
    0xA0,
    0xC0,
    0xA6,
    0xA8,
    0x3F,
    0xD3,
    0x00,
    0xD5,
    0x80,
    0xD9,
    0xF1,
    0xDA,
    0x12,
    0xDB,
    0x40,
    0x20,
    0x02,
    0xA4,
    0xA6,
    )


class State:
    def __init__(self):
        self._iso_select = 0
        self._mode = None
        self._iso_name = None
        self._iso_ls_cache = None
        self.set_mode(MODE_CD)
        
    def inserted_iso(self):
        return self._iso_name
        
    def insert_iso(self):
        self.remove_iso()
        script = os.path.join(APP_DIR, "insert_iso.sh")
        iso_name = self.iso_ls()[self.get_iso_select()]
        self._iso_name = iso_name
        subprocess.check_call((script, iso_name))

    def get_iso_select(self):
        return self._iso_select
        
    def set_iso_select(self, select):
        self._iso_select = select

    def set_iso_select_next(self):
        if self._iso_select == len(self.iso_ls()) - 1:
            return False
        self._iso_select += 1
        return True

    def set_iso_select_prev(self):
        if self._iso_select == 0:
            return False
        self._iso_select -= 1
        return True
        
    def iso_ls(self):
        assert(self._mode == MODE_CD)

        if self._iso_ls_cache:
            return self._iso_ls_cache
        
        script = os.path.join(APP_DIR, "list_iso.sh")
        output = subprocess.check_output((script,))
        iso_list = output.decode().split("\n")
        iso_list = sorted(filter(len, iso_list))
        if len(iso_list) < self._iso_select:
            self._iso_select = 0
        self._iso_ls_cache = iso_list
        return iso_list
        
    def get_mode(self):
        return self._mode
        
    def set_mode(self, mode):
        assert(mode in (MODE_CD, MODE_HDD))
        
        self._iso_name = None
        if mode == MODE_CD:
            script = os.path.join(APP_DIR, "cd_mode.sh")
        elif mode == MODE_HDD:
            script = os.path.join(APP_DIR, "hdd_mode.sh")
        subprocess.check_call([script])
        self._mode = mode
        self._iso_ls_cache = None

    def toogle_mode(self):
        if self.get_mode() == MODE_CD:
            self.set_mode(MODE_HDD)
        else:
            self.set_mode(MODE_CD)
        return self.get_mode()

    def remove_iso(self):
         assert(self._mode == MODE_CD)

         self._iso_name = None
         script = os.path.join(APP_DIR, "remove_iso.sh")
         subprocess.check_call((script,))


class Display:
    def __init__(self):
        disp = SH1106()

        self._disp = disp
        self._font = ImageFont.truetype(FONT, 13)
        self._font_hdd = ImageFont.truetype(FONT, 52)
            
    def refresh(self, state):
        assert(state.get_mode() in (MODE_HDD, MODE_CD))
        
        image = Image.new('1', (self._disp.WIDTH_RES, self._disp.HEIGHT_RES), "WHITE")
        draw = ImageDraw.Draw(image)
        
        if state.get_mode() == MODE_HDD:
            draw.text((0,0), "HDD", font=self._font_hdd)
            self._disp.display_image(image)
            return
        
        iso_name = state.inserted_iso()
        if iso_name == None:
            iso_name = ""
            
        iso_choice = ["", "", ""]
        iso_select = state.get_iso_select()
        iso_ls = state.iso_ls()
        
        if len(iso_ls) == 0:
            iso_choice[1] = "    No ISO"
        else:
            iso_choice[1] = ">" + iso_ls[iso_select]
            try:
                if iso_select > 0:
                    iso_choice[0] = " " + iso_ls[iso_select - 1]
            except IndexError:
                pass
            try:
                iso_choice[2] = " " + iso_ls[iso_select + 1]
            except IndexError:
                pass
        
        draw.text((0,0), "CD " + iso_name, font = self._font)
        draw.text((0,15), iso_choice[0], font = self._font)
        draw.text((0,30), iso_choice[1], font = self._font)
        draw.text((0,45), iso_choice[2], font = self._font)
        self._disp.display_image(image)

    def clear(self):
        image = Image.new('1', (self._disp.WIDTH_RES, self._disp.HEIGHT_RES), "WHITE")
        self._disp.display_image(image)


class WVSButtons:
    def __init__(self):
        self._button_last_time = 0
        self._button_last = 0
        for pin in self.PINS:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def wait_on_button(self):
        while True:
            time.sleep(0.01)
            for pin in self.PINS:
                if not GPIO.input(pin):
                    button_time_d = time.time() - self._button_last_time
                    if self._button_last == pin and button_time_d > 0 and button_time_d < 0.1:
                        continue
                    self._button_last_time = time.time()
                    self._button_last = pin
                    try:
                        return self.BUTTON_NAMES[pin]
                    except KeyError:
                        pass
    
    KEY1 = 21
    KEY2 = 20
    KEY3 = 16
    J_UP = 6
    J_DOWN = 19
    J_LEFT = 5
    J_RIGHT = 26
    J_PRESS = 13
    PINS = (KEY1,
    KEY2,
    KEY3,
    J_UP,
    J_DOWN,
    J_LEFT,
    J_RIGHT,
    J_PRESS,
    )
    BUTTON_NAMES = {
        KEY1 : "mount",
        KEY2 : "umount",
        KEY3 : "mode",
        J_UP : "up",
        J_DOWN : "down",
    }


class Main:
    def __init__(self):
        self._state = State()
        self._display = Display()
        self._display.clear()
        self._display.refresh(self._state)
        self._buttons = WVSButtons()

        self._BUTTON_FUNC = {
            "up" : self._button_up,
            "down" : self._button_down,
            "mount" : self._button_mount,
            "umount" : self._button_umount,
            "mode" : self._button_mode,
        }

    def main(self):
        try:
            while True:
                button = self._buttons.wait_on_button()
                try:
                    f = self._BUTTON_FUNC[button]
                except KeyError:
                    pass
                f()
                self._display.refresh(self._state)
        finally:
            self._display.clear()

    def _button_up(self):
        self._state.set_iso_select_prev()

    def _button_down(self):
        self._state.set_iso_select_next()

    def _button_mode(self):
        self._state.toogle_mode()

    def _button_mount(self):
        self._state.insert_iso()

    def _button_umount(self):
        if self._state.get_mode() != MODE_CD:
            return
        self._state.remove_iso()


if __name__ == "__main__":
    Main().main()



