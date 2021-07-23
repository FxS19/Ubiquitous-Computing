#
# Liniensensor - Robo - Demo 1
# Adafruit CircuitPython 6.2.0
# Board: Metro M4 Express
# Sensoren: KY-033 mit TCRT5000 (3x Digital)
# 28.06.21 - wb
# v0.2
#

import time
import math
import board
from motor import *
from sensor import *

sensors = Sensors([Sensor(board.IO5), Sensor(board.IO6), Sensor(board.IO7), Sensor(board.IO8), Sensor(board.IO9)])

maxSpeed =100  # maximale Geschwindigkeit (0-100)
counter = 0

while True:
    counter+=1
    if counter%1000==0: print(sensors.toString())
    # Fahrtrichtung festlegen
    
    if sensors.read(Sensors.Center) == Sensor.black:
        #print("driveForward")
        motorR(maxSpeed)
        motorL(maxSpeed)

    if sensors.read(Sensors.Left) == Sensor.black:
        motorR(maxSpeed)
        motorL(math.floor(maxSpeed/2))

    if sensors.read(Sensors.LeftLeft) == Sensor.black:
        #print("driveLeft")
        motorR(maxSpeed)
        motorL(0)
        
    if sensors.read(Sensors.Right)==Sensor.black:
        #print("driveRight")
        motorR(math.floor(maxSpeed/2))
        motorL(maxSpeed)

    if sensors.read(Sensors.RightRight) == Sensor.black:
        #print("driveLeft")
        motorR(0)
        motorL(maxSpeed)
