"""Combine sensors to an Array for easier use"""

import board
import time
from sensor import SensorValue, Sensor
from print import print_d

class SensorArrayValue:
    """Value type of Sensor Array"""
    _values = []
    time = 0

    def all(self, color: SensorValue) -> bool:
        """Check if all sensors look like the provided sensor"""
        c = 0
        for sens in self._values:
            if sens == color:
                c += 1
        if c == len(self._values): return True
        return False

    def __init__(self, sensorvalues: SensorValue) -> None:
        self._values = sensorvalues
        self.time = time.monotonic()

    def __str__(self) -> str:
        ret = []
        for value in self._values:
            ret.append(str(value))
        #ret.append("{:.2f}".format(self.time))
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


class SensorArray:
    """All IR sensors combined in one Class"""
    _s = []
    LEFT_LEFT = 4
    LEFT = 3
    CENTER = 2
    RIGHT = 1
    RIGHT_RIGHT = 0
    history_length = 30
    history = [SensorArrayValue([
                SensorValue(SensorValue.WHITE),
                SensorValue(SensorValue.WHITE),
                SensorValue(SensorValue.WHITE),
                SensorValue(SensorValue.WHITE),
                SensorValue(SensorValue.WHITE)
    ])]
    ''' sensor array history:

    [0] = oldest

    len(x) = newest

    [old, , , , , new]'''

    def __init__(self) -> None:
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
        self.update(print_d)
    def read(self, sensor_id) -> SensorValue:
        """
        Read a sensor based on it's name

        Use SensorArray.[LEFT_LEFT, LEFT, CENTER, RIGHT, RIGHT_RIGHT] to index
        """
        return self._s[sensor_id].read()

    def update(self, callback):
        """update all Sensors, if something changed execute the callback function"""
        ret = []
        for s in self._s:
            ret.append(s.read())
        sav = SensorArrayValue(ret)
        if sav != self.history[-1]:
            callback(sav)
            print_d("SENS:", sav)
            if len(self.history) >= self.history_length:
                self.history.pop(0)
            self.history.append(sav)

    def read_all(self):
        """Return all Sensor Values as an Array

        Returns:
            Array<SensorValue>:
            Use SensorArray.[LEFT_LEFT, LEFT, CENTER, RIGHT, RIGHT_RIGHT] to index
        """
        self.update(print_d)
        return self.history

    def __str__(self) -> str:
        ret = []
        for value in self.history:
            ret.append(str(value))
        return "->".join(ret)

    def __getitem__(self, sa_id) -> Sensor:
        return self._s[sa_id]
