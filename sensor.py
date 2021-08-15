
#
# Sensoren
# Board: Metro M4 Express
# AZ-Delivery IR-digital Sensoren
# Group 1
#

from digitalio import DigitalInOut, Direction, Pull
import microcontroller
import time

class SensorValue:
    WHITE = False
    BLACK = True
   
    def __init__(self, value) -> None:
        self.__value = value
    
    def __str__(self) -> str:
        """Return the value of this sensor as a single character String for better Reading"""
        if self.__value:
            return "X"
        else:
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

class SensorArrayValue:
    _values = []
    _time = 0

    def all(self, color: SensorValue) -> bool:
        c = 0
        for sens in self._values:
            if sens == color:
                c += 1
        if c == len(self._values): return True
        return False

    def __init__(self, sensorvalues: SensorValue) -> None:
        self._values = sensorvalues
        self._time = time.monotonic()

    def __str__(self) -> str:
        ret = []
        for value in self._values:
            ret.append(str(value))
        return " ".join(ret)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SensorValue):
            return self.all(other)
        elif isinstance(other, bool):
            return self.all(SensorValue(other))
        elif isinstance(other, SensorArrayValue):
            ok = True
            for id, selfvalue in enumerate(self._values):
                if selfvalue != other[id] and ok:
                    ok = False
            return ok
        else:
            NotImplemented

    def __getitem__(self, id):
        return self._values[id]

    def get_time_difference(self, other):
        if isinstance(other, SensorArrayValue):
            return abs(self._time - other._time)
        else:
            NotImplemented


class SensorArray:
    """All IR sensors combined in one Class"""
    _s = []
    LEFT_LEFT = 4
    LEFT = 3
    CENTER = 2
    RIGHT = 1
    RIGHT_RIGHT = 0
    history_length = 10
    history = [SensorArrayValue([
                SensorValue(SensorValue.WHITE), 
                SensorValue(SensorValue.WHITE),
                SensorValue(SensorValue.WHITE),
                SensorValue(SensorValue.WHITE),
                SensorValue(SensorValue.WHITE)
    ])]

    def __init__(self, sensors) -> None:
        """All IR sensors

        Args:
            sensors (Array<Sensor>): All Sensors
        """
        self._s=sensors
        self.update()
    def read(self, id) -> SensorValue:
        """
        Read a sensor based on it's name

        Use SensorArray.[LEFT_LEFT, LEFT, CENTER, RIGHT, RIGHT_RIGHT] to index
        """
        return self._s[id].read()

    def update(self):
        ret = []
        for s in self._s:
            ret.append(s.read())
        sav = SensorArrayValue(ret)
        if sav != self.history[-1]:
            if len(self.history) >= self.history_length:
                self.history.pop(0)
            self.history.append(sav)
            print("SENS:", str(sav))

    def read_all(self):
        """Return all Sensor Values as an Array

        Returns:
            Array<SensorValue>: Use SensorArray.[LEFT_LEFT, LEFT, CENTER, RIGHT, RIGHT_RIGHT] to index
        """
        self.update()     
        return self.history
    
    def __str__(self) -> str:
        ret = []
        for value in self.history:
            ret.append(str(value))
        return "->".join(ret)

    def __getitem__(self, id) -> Sensor:
        return self._s[id]
