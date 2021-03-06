"""
Provide a basic playground

use:
from debug import *
to start
"""
import board
import neopixel
from driveByMatrix import DriveByMatrix

driver = DriveByMatrix("drive", neopixel.NeoPixel(board.NEOPIXEL, 1))

def start_update():
    """Perform sensor and motor updates in a loop"""
    driver.start()
