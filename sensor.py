"""
Sensoren
Board: Metro M4 Express
AZ-Delivery IR-digital Sensoren
Group 1
"""

from digitalio import DigitalInOut, Direction, Pull
import microcontroller


class SensorValue:
    """Value type of IR sensor"""
    WHITE = False
    BLACK = True

    def __init__(self, value) -> None:
        self.__value = value

    def __str__(self) -> str:
        """Return the value of this sensor as a single character String for better Reading"""
        if self.__value:
            return "X"
        return "-"

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
