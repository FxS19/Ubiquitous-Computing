"""Combine sensors to an Array for easier use"""


from micropython import const
import board
import time
from sensor import SensorValue, Sensor
from print import print_d

__EMPTY_SENSORVALUE = SensorValue(SensorValue.WHITE)

class SensorArrayValue:
    """Value type of Sensor Array"""
    _values = []
    time = 0
    __end_time = -1.0

    def all(self, color: SensorValue) -> bool:
        """Check if all sensors look like the provided sensor"""
        c = 0
        for sens in self._values:
            if sens == color:
                c += 1
        if c == len(self._values):
            return True
        return False

    def __init__(self, sensorvalues: SensorValue) -> None:
        self._values = sensorvalues
        self.time = time.monotonic()

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
            for value_id, selfvalue in enumerate(self._values):
                if selfvalue != other[value_id] and ok:
                    ok = False
            return ok
        NotImplemented

    def __getitem__(self, sav_id):
        return self._values[sav_id]

    def get_time_difference(self, other):
        """return the difference of time between this and another SensorArrayValue"""
        if isinstance(other, SensorArrayValue):
            return self.time - other.time
        elif isinstance(other, int):
            return self.time - other
        NotImplemented

    def set_end_time(self, time: float):
        "Set when this value has ended, needs to be set at higher code level"
        self.__end_time = time
    
    def get_end_time(self):
        "return time when this value has ended, return time.monotonic if still active"
        return self.__end_time if self.__end_time != -1.0 else time.monotonic()


class SensorArray:
    """All IR sensors combined in one Class"""
    _s = []
    LEFT_LEFT = const(0)
    LEFT = const(1)
    CENTER = const(2)
    RIGHT = const(3)
    RIGHT_RIGHT = const(4)
    history_length = 30
    history = []

    ''' sensor array history:

    [0] = oldest

    len(x) = newest

    [old, , , , , new]'''

    def __init__(self, history_length = 30) -> None:
        """All IR sensors

        Args:
            sensors (Array<Sensor>): All Sensors
        """
        self._s = [
            Sensor(board.IO9),
            Sensor(board.IO8),
            Sensor(board.IO7),
            Sensor(board.IO6),
            Sensor(board.IO5)]
        self.history = [
            SensorArrayValue([__EMPTY_SENSORVALUE] * 5)
        ] * history_length
        self.history_length = history_length
        self.update(print_d)

    def read(self, sensor_id) -> SensorValue:
        """
        Read a sensor based on it's name

        Use SensorArray.[LEFT_LEFT, LEFT, CENTER, RIGHT, RIGHT_RIGHT] to index
        """
        return self._s[sensor_id].read()

    def update(self, callback=lambda _: None):
        """update all Sensors, if something changed execute the callback function"""
        ret = []
        for s in self._s:
            ret.append(s.read())
        sav = SensorArrayValue(ret)
        if sav != self.history[-1]:
            if sav == SensorValue.WHITE and sav.get_time_difference(self.history[-1]) <= 0.1: 
                # Filter bad sensor values, sometimes there is nothing visible. But in reality there is a Line.
                # ignore these short periods
                return
            #print_d("SENS:", sav)
            self.history.pop(0)
            self.history[-1].set_end_time(sav.time)
            self.history.append(sav)
            callback(sav)

    def read_all(self):
        """Return all Sensor Values as an Array

        Returns:
            Array<SensorValue>:
            Use SensorArray.[LEFT_LEFT, LEFT, CENTER, RIGHT, RIGHT_RIGHT] to index
        """
        self.update()
        return self.history

    def __str__(self) -> str:
        ret = []
        for value in self.history:
            ret.append(str(value))
        return "->".join(ret)

    def __getitem__(self, sa_id) -> Sensor:
        return self._s[sa_id]
