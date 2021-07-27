
#
# Sensoren
# Board: Metro M4 Express
# AZ-Delivery IR-digital Sensoren
# Group 1
#

from digitalio import DigitalInOut, Direction, Pull
import microcontroller

class SensorValue:
    WHITE = False
    BLACK = True
   
    def __init__(self, value) -> None:
        self.__value = value
    
    def __str__(self) -> str:
        """Return the value of this sensor as a single character String for better Reading"""
        if self.__value:
            return " "
        else:
            return "x"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, bool):
            return self.__value == o
        if not isinstance(o, SensorValue):
            return NotImplemented
        return self.__value == o.__value


class Sensor:
    """One IR Sensor"""
    _sensor = 0
    def __init__(self, sensor: microcontroller.Pin) -> None:
        """Create one Sensor, based on the IO Pin

        Args:
            sensor (board.IO): IO pin
        """
        s = DigitalInOut(sensor)
        s.direction = Direction.INPUT
        s.pull = Pull.UP
        self._sensor = s
    
    def read(self) -> SensorValue:
        """Return the Value of this Sensor"""
        return SensorValue(self._sensor.value)
    
    def __str__(self):
        """Return the value of this sensor as a single character String for better Reading"""
        return str(self.read())
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, SensorValue):
            return self.read() == o
        if not isinstance(o, Sensor):
            return NotImplemented
        return self.read() == o.read()

class SensorArray:
    """All IR sensors combined in one Class"""
    _s = []
    LEFT_LEFT = 0
    LEFT = 1
    CENTER = 2
    RIGHT = 3
    RIGHT_RIGHT = 4

    def __init__(self, sensors) -> None:
        """All IR sensors

        Args:
            sensors (Array<Sensor>): All Sensors
        """
        self._s=sensors
    def read(self, id) -> SensorValue:
        """
        Read a sensor based on it's name

        Use SensorArray.[LEFT_LEFT, LEFT, CENTER, RIGHT, RIGHT_RIGHT] to index
        """
        return self._s[id].read()
    def read_all(self):
        """Return all Sensor Values as an Array

        Returns:
            Array<SensorValue>: Use SensorArray.[LEFT_LEFT, LEFT, CENTER, RIGHT, RIGHT_RIGHT] to index
        """
        ret = []
        for s in self._s:
            ret.append(s.read())
        return ret
    
    def __str__(self) -> str:
        ret = []
        for sensor in self._s:
            ret.append(str(sensor.read()))
        return " ".join(ret)
