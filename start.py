"""
Line following program
Adafruit CircuitPython 6.2.0
Board: Metro ESP32 S2 BETA
Sensoren: KY-033 mit TCRT5000 (3x Digital)
"""

import time
import board
from print import print_d
from display import Display
import neopixel

# Rotary encoder
import rotaryio
import digitalio

# Setup rotary encoder
button = digitalio.DigitalInOut(board.IO10)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
encoder = rotaryio.IncrementalEncoder(board.IO11, board.IO12)
button_state = None
last_position = encoder.position


# init NEOPIXEL
pixel_onboard = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel_onboard.brightness = 0.5
i2c = board.I2C()
display = Display(i2c, pixel_onboard)

update_screen = True
settings_change_value = False

while True:
    # test for button press on rotary encoder
    menue_item = display.menue_item

    if not button.value and button_state is None:
        button_state = time.monotonic()
    if button.value and button_state != None:
        update_screen = True
        if time.monotonic() - button_state > 1:
            # long press
            if "execute" in display.menue_items[menue_item]:
                display.menue_items[menue_item]["execute"](display.menue_items[menue_item]["value"])
        else:
            # short press
            settings_change_value = not settings_change_value
        print_d("Button pressed.", time.monotonic() - button_state)
        button_state = None

    current_position = encoder.position
    position_change = current_position - last_position

    if position_change != 0:
        print_d("ENC:", current_position)
        update_screen = True
        if settings_change_value is True:
            current_menue_item_value = display.menue_items[menue_item]["value"]
            if type(current_menue_item_value) == bool:
                display.menue_items[menue_item]["value"] = not current_menue_item_value
            elif type(current_menue_item_value) == int:
                display.menue_items[menue_item]["value"] += position_change
            elif type(current_menue_item_value) == str:
                if current_menue_item_value == "drive":
                    display.menue_items[menue_item]["value"] = "race"
                elif current_menue_item_value == "race":
                    display.menue_items[menue_item]["value"] = "drive"
            elif type(current_menue_item_value) == float:
                display.menue_items[menue_item]["value"] += position_change * 0.01
            else:
                print_d("Error: settings type not found")
            # Call callback if available
            if display.menue_items[menue_item]["callback"]:
                display.menue_items[menue_item]["callback"](display.menue_items[menue_item]["value"])
                print_d("Set: ", display.menue_items[menue_item]["name"], display.menue_items[menue_item]["value"])
        else:
            display.menue_item += position_change
            while display.menue_item < 0:
                display.menue_item = len(display.menue_items) + display.menue_item
            while display.menue_item > len(display.menue_items) - 1:
                display.menue_item = display.menue_item - len(display.menue_items)

    if update_screen:
        update_screen = False
        display.show_settings(change_value=settings_change_value)

    last_position = current_position
