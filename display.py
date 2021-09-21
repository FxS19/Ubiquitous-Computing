
import time
import storage
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import print
from driver import Driver

class Display:
    def __init__ (self, i2c, neopixel):
        # Setup display´
        displayio.release_displays()
        self.i2c = i2c
        self.display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
        self.display = adafruit_displayio_ssd1306.SSD1306(self.display_bus, width=128, height=64)

        # prepare display
        splash = displayio.Group()
        self.display.show(splash)
        color_bitmap = displayio.Bitmap(128, 64, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0  # Black
        self.bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
        splash.append(self.bg_sprite)

        self.__neopixel = neopixel
        self.mode = "menu"
        self.menue_item = 0
        self.menue_items = [
            {
                "name": "Start",
                "value": "drive",
                "callback": lambda _:None,
                "execute": self.do_drive
            },
            {
                "name": "debug",
                "value": print.get_debug_mode(),
                "callback": self.update_debug_mode
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

        # display text
        self.text_area = label.Label(terminalio.FONT, text="", color=0xffffff, x=0, y=4)
        splash.append(self.text_area)

    def do_drive(self, mode):
        """start driving"""
        driver = Driver(mode=mode, neopixel=self.__neopixel)
        for x in range(5, 0, -1):
            self.text_area.text = str(x)
            time.sleep(1)
        self.text_area.text = "GO!!!\n" + driver.mode
        driver.start() #force regular updates

    def change_write_mode(self, value: bool):
        """Change the write permission of the internal filesystem"""
        try:
            storage.remount("/", not value)
        except RuntimeError:
            self.text_area.text = "Not possible!\nComputer is connected"
            time.sleep(1)

    def update_debug_mode(self, value: bool):
        """change if debug messages will be displayed or not"""
        try:
            print.set_debug_mode(value)
        except OSError:
            self.text_area.text = "Not possible!\nEnable r/w first"
            time.sleep(1)

    def show_settings(self, change_value):
        """Display all visible setting entries"""
        items_to_display = 4
        if (items_to_display > len(self.menue_items) - self.menue_item):
            items_to_display = len(self.menue_items) - self.menue_item
        visible_items = self.menue_items[self.menue_item: self.menue_item + items_to_display]
        my_text = ""
        for i, v in enumerate(visible_items):
            if i == 0:
                if change_value == True:
                    my_text += ">"
                my_text += "> "
            else:
                my_text += "  "
            my_text += v["name"] + ": " + str(v["value"]) + "\n"
        self.text_area.text = my_text