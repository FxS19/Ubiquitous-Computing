"""Provide features for better detecting lines"""

from sensor import SensorValue
from sensorarray import SensorArrayValue

class Line:
    """Functions for detecting the line inside a SensorArrayValue"""
    def is_something(array_value: SensorArrayValue):
        """test if there is some kind of line"""
        return array_value != SensorValue.WHITE

    def get_bar(array_value: SensorArrayValue):
        """Get the position and the width of the line.
        If there are multiple possible answers the first thickest line is selected."""
        ctr = 0
        max_ctr = 0
        begin = 0
        begin_max = 0
        for s_id, sensor in enumerate(array_value):
            if sensor == SensorValue.BLACK:
                ctr += 1
                if ctr > max_ctr:
                    max_ctr = ctr
                    begin_max = begin
            else:
                ctr = 0
                begin = s_id + 1
        if max_ctr == 0:
            return (0, 0)
        return (begin_max, max_ctr)

    def get_bar_width(array_value: SensorArrayValue):
        """Return the number of sensors that are active in one row"""
        _, max_value = Line.get_bar(array_value)
        return max_value

    def get_bar_position(array_value: SensorArrayValue):
        """Return between 0 and 4"""
        begin_max, max_length = Line.get_bar(array_value)
        if max_length % 2 == 1:
            return begin_max + (max_length - 1) / 2.0
        return begin_max + max_length / 2.0 - 0.5
