"""
Line following program
Adafruit CircuitPython 6.2.0
Board: Metro ESP32 S2 BETA
Sensoren: KY-033 mit TCRT5000 (3x Digital)
28.06.21 - wb
v0.2
"""

import time
import board
import storage
from print import print_d, set_debug_mode, get_debug_mode
from motor import Motor, Vehicle
from driver import Driver, Line
from sensor import SensorArray, Sensor, SensorArrayValue, SensorValue
import neopixel

# Display
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

# Rotary encoder
import rotaryio
import digitalio

# Define working variables
max_execution_time = 0.05
timer = 0
last_second = 0

# Setup rotary encoder
button = digitalio.DigitalInOut(board.IO10)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
encoder = rotaryio.IncrementalEncoder(board.IO11, board.IO12)
button_state = None
last_position = encoder.position


# Setup display´
displayio.release_displays()
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)
splash = displayio.Group()
display.show(splash)
color_bitmap = displayio.Bitmap(128, 64, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0  # Black

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Init Sensors
sensor_array = SensorArray([
    Sensor(board.IO9),
    Sensor(board.IO8),
    Sensor(board.IO7),
    Sensor(board.IO6),
    Sensor(board.IO5)])

# Init motors
vehicle = Vehicle(
    motor_l=Motor(io_pin_fwd=board.IO14, io_pin_bwd=board.IO13),
    motor_r=Motor(io_pin_fwd=board.IO15, io_pin_bwd=board.IO16))


# init NEOPIXEL
pixel_onboard = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel_onboard.brightness = 0.5

def do_drive(mode):
    # start driving
    timer = 0
    driver = Driver(sensor_array, vehicle=vehicle, alarm_sec=max_execution_time, mode=mode)
    for x in range(5, 0, -1):
        text_area.text = str(x)
        time.sleep(1)
    text_area.text = "GO!!!\n" + driver.mode
    while True:
        sensor_array.update(driver.sens_update_callback)
        driver.update() #force regular updates
        vehicle.update()

        if time.monotonic() - timer > max_execution_time:
            pixel_onboard[0] = (255, 0, 0)
        elif driver.get_corner():
            pixel_onboard[0] = (0, 128, 0)
        elif driver.sensor_array.history[-1] == SensorValue.WHITE:
            pixel_onboard[0] = (0, 0, 128)
        else:
            pixel_onboard[0] = (0, 0, 0)
        timer = time.monotonic()

def change_write_mode(value: bool):
    try:
        storage.remount("/", not value)
    except RuntimeError:
        text_area.text = "Not possible!\nComputer is connected"
        time.sleep(1)

def update_debug_mode(value: bool):
    try:
        set_debug_mode(value)
    except OSError:
        text_area.text = "Not possible!\nEnable r/w first"
        time.sleep(1)

mode = "menu"
menue_item = 0
menue_items = [
    {
        "name": "Start",
        "value": "drive",
        "callback": lambda _:None,
        "execute": do_drive
    },
    {
        "name": "debug",
        "value": get_debug_mode(),
        "callback": update_debug_mode
    },
    {
        "name": "test",
        "value": 0,
        "callback": print_d
    },
    {
        "name": "int. r/w",
        "value": False,
        "callback": change_write_mode
    }

]

text_area = label.Label(terminalio.FONT, text="", color=0xffffff, x=0, y=4)
splash.append(text_area)

def print_settings():
    items_to_display = 4
    if (items_to_display > len(menue_items) - menue_item):
        items_to_display = len(menue_items) - menue_item
    visible_items = menue_items[menue_item: menue_item + items_to_display]
    my_text = ""
    for i, v in enumerate(visible_items):
        if i == 0:
            if settings_change_value == True:
                my_text += ">"
            my_text += "> "
        else:
            my_text += "  "
        my_text += v["name"] + ": " + str(v["value"]) + "\n"
    text_area.text = my_text


settings_change_value = False
update_screen = True
while True:
    # test for button press on rotary encoder
    if not button.value and button_state is None:
        button_state = time.monotonic()
    if button.value and button_state != None:
        update_screen = True
        if time.monotonic() - button_state > 1:
            # long press
            if "execute" in menue_items[menue_item]:
                menue_items[menue_item]["execute"](menue_items[menue_item]["value"])
        else:
            # short press
            settings_change_value = not settings_change_value
        print_d("Button pressed.", time.monotonic() - button_state)
        button_state = None

    current_position = encoder.position
    position_change = current_position - last_position

    if position_change != 0:
        print_d("ENC:",current_position)
        update_screen = True
        if settings_change_value == True:
            if type(menue_items[menue_item]["value"]) == bool:
                menue_items[menue_item]["value"] = not menue_items[menue_item]["value"]
            elif type(menue_items[menue_item]["value"]) == int:
                menue_items[menue_item]["value"] += position_change
            elif type(menue_items[menue_item]["value"]) == str:
                if menue_items[menue_item]["value"] == "drive":
                    menue_items[menue_item]["value"] = "race"
                elif menue_items[menue_item]["value"] == "race":
                    menue_items[menue_item]["value"] = "drive"
            else:
                print_d("Error: settings type not found")
            # Call callback if available
            if menue_items[menue_item]["callback"]:
                menue_items[menue_item]["callback"](menue_items[menue_item]["value"])
                print_d("Set: ", menue_items[menue_item]["name"], menue_items[menue_item]["value"])
        else:
            menue_item += position_change
            while menue_item < 0:
                menue_item = len(menue_items) + menue_item
            while menue_item > len(menue_items) - 1:
                menue_item =  menue_item - len(menue_items)

    if update_screen:
        update_screen = False
        print_settings()

    last_position = current_position