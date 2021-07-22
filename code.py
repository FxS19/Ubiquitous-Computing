#
# Liniensensor - Robo - Demo 1
# Adafruit CircuitPython 6.2.0
# Board: Metro M4 Express
# Sensoren: KY-033 mit TCRT5000 (3x Digital)
# 28.06.21 - wb
# v0.2
#

import time
import board
from digitalio import DigitalInOut, Direction, Pull
from motor import *

sensor1 = DigitalInOut(board.D2)
sensor1.direction = Direction.INPUT
sensor1.pull = Pull.UP

sensor2 = DigitalInOut(board.D3)
sensor2.direction = Direction.INPUT
sensor2.pull = Pull.UP

sensor3 = DigitalInOut(board.D4)
sensor3.direction = Direction.INPUT
sensor3.pull = Pull.UP

maxSpeed = 25  # maximale Geschwindigkeit (0-100)

while True:

    sensorWert_R = sensor1.value  # rechter Sensor
    sensorWert_M = sensor2.value  # mittlerer Sensor
    sensorWert_L = sensor3.value  # linker Sensor

    #print(sensorWert_L, sensorWert_M, sensorWert_R)
    #time.sleep(0.25)

    # Fahrtrichtung festlegen
    if sensorWert_M == 0:
        #print("driveForward")
        motorR(maxSpeed)
        motorL(maxSpeed)

    if sensorWert_L == 0:
        #print("driveLeft")
        motorR(maxSpeed)
        motorL(0)

    if sensorWert_R == 0:
        #print("driveRight")
        motorR(0)
        motorL(maxSpeed)



