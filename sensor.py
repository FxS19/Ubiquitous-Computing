
#
# Sensoren
# Board: Metro M4 Express
# AZ-Delivery IR-digital Sensoren
# Gruppe 1
#

from digitalio import DigitalInOut, Direction, Pull

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
            return " "
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
