from print import print_d
from sensorarray import SensorArrayValue, SensorArray
import time
from line import Line
from sensor import SensorValue

class RecognizeShapes:
    def get_corner(sensor_array: SensorArray, min_bar_width = 2, max_look_back_sec = 2) -> (bool(False) or SensorArrayValue):
            """Search the history, if there is some kind of corner visible.
            If the robot has not found the line again this function will
            return the sensor values of that specific corner."""
            now = time.monotonic()
            lost_line_after_corner = False
            border_id = 0
            for sav_id, sav in enumerate(reversed(sensor_array.history)):
                if now - sav.time > max_look_back_sec:
                    return False # No corner the last ... sec
                if Line.get_bar_width(sav) > min_bar_width: # detected first corner
                    border_id = sav_id
                    break # no need for further investigation

            test_pice = sensor_array.history[-(border_id+1):len(sensor_array.history)]
            #first value is corner

            corner_detected = False
            for sav_id, sav, in enumerate(test_pice):
                if Line.get_bar_width(sav) > min_bar_width and abs(Line.get_bar_position(sav) - 2) >= 0.5:
                    # Test if this looks like a corner
                    corner_detected = True
                if corner_detected and sav == SensorValue.WHITE:
                    lost_line_after_corner = True
                if lost_line_after_corner and abs(Line.get_bar_position(sav) - 2) <= 1:
                    return False #lost line, but is is now near center again
                if sav.time - test_pice[0].time >= 0.2 and abs(Line.get_bar_position(sav) - 2) <= 2:
                    return False #line is there and time since corner is high enough
            if corner_detected:
                return test_pice[0]
            return False
    
    def trend(sensor_array: SensorArray, values: int) -> float:
        """Get the trend following the line for the last x values. 
        Return range from left to right, negative values represent a trend to the left side
        """
        now = time.monotonic()
        cooldown = 1 # > old values are less relevant
        trend_array = [] # [0] = most recent value
        sav_length = len(sensor_array.history)
        for i in range(sav_length):
            if i > sav_length - 1:
                break
            current_sav = sensor_array.history[sav_length - (i+1)]
            cooldown_factor = (now - current_sav.time) * cooldown
            if cooldown_factor == 0:
                # prevent div by 0
                cooldown_factor = 1
            if Line.is_something(current_sav):
                trend_array.append([(Line.get_bar_position(current_sav) - 2),  cooldown_factor])
            else:
                return 0
                for k in range(i+1, sav_length):
                    current_sav = sensor_array.history[sav_length - (k+1)]
                    if Line.is_something(current_sav):
                        trend_array.append([(Line.get_bar_position(current_sav) - 2),  cooldown_factor])
                        break
                
            if len(trend_array) == values:
                break
        trend = 0
        if len(trend_array) < 2:
            return 0 # not enough values collected to calculate a trend
        for trend_id in range(1,len(trend_array)):
            # links < rechts            ((t-1) - (t)) / cooldown(t)
            trend += ((trend_array[trend_id][0] - trend_array[trend_id - 1][0]) / trend_array[trend_id][1])
        return trend
