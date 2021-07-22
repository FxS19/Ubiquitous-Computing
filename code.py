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

class Sensor:
    white = False
    black = True
    _sensor = 0
    def __init__(self, sensor) -> None:
        s = DigitalInOut(sensor)
        s.direction = Direction.INPUT
        s.pull = Pull.UP
        self._sensor = s
    def read(self):
        return self._sensor.value
    def toString(self):
        if self.read():
            return "0"
        else:
            return "x"

class Sensors:
    _s = []
    LeftLeft = 0
    Left = 1
    Center = 2
    Right = 3
    RightRight = 4

    def __init__(self, sensors) -> None:
        self._s=sensors
    def read(self, id):
        return self._s[id].read()
    def read_all(self):
        ret = []
        for s in self._s:
            ret.append(s.read())
        return ret
    def toString(self):
        ret = []
        for s in self._s:
            ret.append(s.toString())
        return ret


sensor = [Sensor(board.D1), Sensor(board.D2), Sensor(board.D3), Sensor(board.D4), Sensor(board.D5)]
sensors = Sensors(sensor)

maxSpeed =100  # maximale Geschwindigkeit (0-100)

while True:

    values = sensors.read_all()

    #if (sensorWert_L):

    print(sensors.toString())
    #print(sensorWert_L, sensorWert_M, sensorWert_R)
    #time.sleep(0.25)

    # Fahrtrichtung festlegen
    
    if sensors.read(Sensors.Center) == Sensor.black:
        #print("driveForward")
        motorR(maxSpeed)
        motorL(maxSpeed)

    if sensors.read(Sensors.LeftLeft) == Sensor.black or sensors.read(Sensors.Left) == Sensor.black:
        #print("driveLeft")
        motorR(maxSpeed)
        motorL(0)

    if sensors.read(Sensors.RightRight) == Sensor.black or sensors.read(Sensors.Right)==Sensor.black:
        #print("driveRight")
        motorR(0)
        motorL(maxSpeed)


