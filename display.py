"""Display functions"""

import time
import storage
import adafruit_ssd1306
import print
from settingStorage import SettingStorage


class Display:
    i2c = None
    oled = None

    def __init__(self, i2c, neopixel):

        # Setup display
        self.i2c = i2c
        
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c)

        self.oled.fill(0)
        self.oled.show()

        self.__neopixel = neopixel
        self.mode = "menu"
        self.menue_item = 0
        self.menue_items = [
            {
                "name": "Drive",
                "value": "",
                "callback": lambda _: None,
                "execute": self.do_new_drive
            },
            {
                "name": "linear_agg",
                "value": float(SettingStorage.get_value("linear_aggressiveness")),
                "callback": self.get_save_function("linear_aggressiveness")
            },
            {
                "name": "cubic_agg",
                "value": float(SettingStorage.get_value("cubic_aggressiveness")),
                "callback": self.get_save_function("cubic_aggressiveness")
            },
            {
                "name": "corner_9_s",
                "value": float(SettingStorage.get_value("corner_9_short_modifier")),
                "callback": self.get_save_function("corner_9_short_modifier")
            },
            {
                "name": "corner_9_l",
                "value": float(SettingStorage.get_value("corner_9_long_modifier")),
                "callback": self.get_save_function("corner_9_long_modifier")
            },
            {
                "name": "corner_h_s",
                "value": float(SettingStorage.get_value("corner_h_short_modifier")),
                "callback": self.get_save_function("corner_h_short_modifier")
            },
            {
                "name": "corner_h_l",
                "value": float(SettingStorage.get_value("corner_h_long_modifier")),
                "callback": self.get_save_function("corner_h_long_modifier")
            },
            {
                "name": "drv_o_c_s",
                "value": float(SettingStorage.get_value("drive_over_corner_seconds")),
                "callback": self.get_save_function("drive_over_corner_seconds")
            },
            {
                "name": "Drive_old",
                "value": "drive",
                "callback": lambda _: None,
                "execute": self.do_old_drive
            },
            {
                "name": "debug",
                "value": print.get_debug_mode(),
                "callback": self.get_save_function("debug")
            },
            {
                "name": "test",
                "value": 0,
                "callback": print.print_d
            },
            {
                "name": "int. r/w",
                "value": False,
                "callback": self.change_write_mode
            }
        ]

    def do_old_drive(self, mode):
        """start driving with code from 1st part"""
        from driveByMatrix import DriveByMatrix
        driver = DriveByMatrix(mode=mode, neopixel=self.__neopixel)
        for x in range(5, 0, -1):
            self.display_center_text("   " + str(x))
            time.sleep(1)
        self.display_center_text("GO!!!\n" + driver.mode)
        driver.start()  # force regular updates (will run forever)

    def do_new_drive(self, value):
        """Start new driving mode"""
        from drive import Drive
        driver = Drive(neopixel=self.__neopixel)
        for x in range(5, 0, -1):
            self.display_center_text("   " + str(x))
            # time.sleep(1)
        self.display_center_text("GO!")
        driver.start()  # force regular updates

    def change_write_mode(self, value: bool):
        """Change the write permission of the internal filesystem"""
        try:
            storage.remount("/", not value)
        except RuntimeError:
            self.display_error_message("Not possible!\nComputer is connected", 1)

    def get_save_function(self, key: str) -> function:
        """Get a function for saving a not jet known value to a defined storage space"""
        def __tmp(value):
            self.save_value(key, str(value))
        return __tmp

    def save_value(self, key: str, value: str):
        """Save value to a known storage space"""
        try:
            SettingStorage.set_value(key, value)
        except OSError:
            self.display_error_message("Not possible!\nEnable r/w first", 1)

    def display_center_text(self, message: str):
        self.oled.fill(0)
        self.oled.text("{0}".format(message), 40, 20, 1)
        self.oled.show()

    def display_error_message(self, message : str, seconds: int):
        self.oled.fill(0)
        self.oled.text("{0}".format(message), 2, 20, 1)
        self.oled.invert(True)
        self.oled.show()
        time.sleep(seconds)
        self.oled.fill(0)
        self.oled.show()
        self.oled.invert(False)

    def show_settings(self, change_value):
        """Display all visible setting entries"""
        self.oled.fill(0)
        items_to_display = 5
        if (items_to_display > len(self.menue_items) - self.menue_item):
            items_to_display = len(self.menue_items) - self.menue_item
        visible_items = self.menue_items[self.menue_item: self.menue_item + items_to_display]
        for i, v in enumerate(visible_items):
            my_text = ""
            if i == 0:
                if change_value is True:
                    my_text += ">"
                my_text += "> "
            else:
                my_text += "  "
            if (type(v["value"]) == float):
                my_text += v["name"] + ": " + "{:.2f}".format(v["value"]) + "\n"
            else:
                my_text += v["name"] + ": " + str(v["value"]) + "\n"
            self.oled.text("{0}".format(my_text), 0, i*12, 1)
        self.oled.show() 
