from print import print_d
from sensorarray import SensorArrayValue
from sensorarray import SensorArray
import time
from line import Line
from sensor import SensorValue


class RecognizeShapes:
    def get_corner(sensor_array: SensorArray, min_bar_width=2, max_look_back_sec=2) -> (bool(False) or SensorArrayValue):
        """Search the history, if there is some kind of corner visible.
        If the robot has not found the line again this function will
        return the sensor values of that specific corner."""
        now = time.monotonic()
        lost_line_after_corner = False
        border_id = 0
        for sav_id, sav in enumerate(reversed(sensor_array.history)):
            if now - sav.time > max_look_back_sec:
                return False  # No corner the last ... sec
            if Line.get_bar_width(sav) > min_bar_width:  # detected first corner
                border_id = sav_id
                break  # no need for further investigation

        test_pice = sensor_array.history[-(border_id + 1):len(sensor_array.history)]
        # first value is corner

        corner_detected = False
        for sav_id, sav, in enumerate(test_pice):
            if Line.get_bar_width(sav) > min_bar_width and abs(Line.get_bar_position(sav) - 2) >= 0.5:
                # Test if this looks like a corner
                corner_detected = True
            if corner_detected and sav == SensorValue.WHITE:
                lost_line_after_corner = True
            if lost_line_after_corner and abs(Line.get_bar_position(sav) - 2) <= 1:
                return False  # lost line, but is is now near center again
            if sav.time - test_pice[0].time >= 0.2 and abs(Line.get_bar_position(sav) - 2) <= 2:
                return False  # line is there and time since corner is high enough
        if corner_detected:
            return test_pice[0]
        return False

    def detect_corner_shape(sensor_array: SensorArray, max_look_back_sec=2) -> str:
        """Get the type of corner if some\n
        '' = nothing\n
        'tl' = T-crossing on the left\n
        'tr' = T-crossing on the right\n
        '9l' = 90° left\n
        '9r' = 90° right\n
        'hl' = hard left\n
        'hr' = hard right"""
        now = time.monotonic()
        min_bar_width = 2

        results = [(-1,0)]  # [0] newest
        detected_patterns = [False, False, False, False, False, False]

        def __append_type(i, tiemestamp):
            if results[-1][0] != i:
                results.append((i, tiemestamp))
                detected_patterns[i] = True
            elif results[-1][1] > tiemestamp:
                results[-1] = (i, tiemestamp)

        averageLinePosition = RecognizeShapes.average_line_position(sensor_array, max_look_back_sec)

        # 0: nothing
        # 1: single line
        # 2: corner l
        # 3: corner r
        # 4: split l
        # 5: split r

        # analyse history and detect sensor patterns
        for sav in reversed(sensor_array.history):
            if now - sav.time > max_look_back_sec:
                break  # stop analyzing if time target is reached
            if Line.get_bar_count(sav) > 1:
                bar1 = Line.get_bar_position(Line.get_line(sav, 1)) - 2
                bar2 = Line.get_bar_position(Line.get_line(sav, 2)) - 2
                if abs(bar1) - abs(averageLinePosition) > abs(bar2) - abs(averageLinePosition):  # left corner
                    __append_type(4, sav.time)
                else:
                    __append_type(5, sav.time)
            elif Line.is_something(sav):
                if Line.get_bar_width(sav) > min_bar_width:  # perfect 90° corner visible
                    if Line.get_bar_position(sav) >= 2:  # no decision possible based on average line position
                        __append_type(3, sav.time)
                    else:
                        __append_type(2, sav.time)
                else:
                    __append_type(1, sav.time)
            else:
                __append_type(0, sav.time)

        results.pop(0)  # get rid of start value

        if len(results) == 0: # stop if no value visible
            return ''

        if results[0][0] == 0:  # newest value is nothing
            if detected_patterns[4] or detected_patterns[5]:  # a line split was visible
                if detected_patterns[4]:
                    return 'hl'
                return 'hr'
            if detected_patterns[3] and detected_patterns[2]: # there was a corner on the left and right
                return 'tr' # t crossing center, but tr also works
            if detected_patterns[3]:  # there was a corner on the right
                return '9r'
            if detected_patterns[2]:  # there was a corner on the left
                return '9l'

        if detected_patterns[4] and detected_patterns[5]: # a line split on the left and right was visible
            return 'tr' # 4-way crossing from an weird angle
        if  detected_patterns[2] and detected_patterns[3] and results[0][0] == 1 and now - results[0][1] > 0.3: # there was a corner on the left and right, now there is a single line since more the x seconds
            return 'tr' # 4-way crossing

        if detected_patterns[4] or detected_patterns[5]:  # a line split was visible
            if results[0][0] == 1 and now - results[0][1] > 0.3:  # newest value is single line and older then x sec
                if detected_patterns[4]:
                    return 'tl'
                return 'tr'
        if detected_patterns[3] or detected_patterns[2]: # there was a corner on the left or right
            if results[0][0] == 1 and now - results[0][1] > 0.3:  # newest value is single line and older then x sec
                if detected_patterns[2]:
                    return 'tl'
                return 'tr'

        return ''

    def trend(sensor_array: SensorArray, values: int) -> float:
        """Get the trend following the line for the last x values.
        Return range from left to right, negative values represent a trend to the left side
        """
        now = time.monotonic()
        cooldown = 1  # > old values are less relevant
        trend_array = []  # [0] = most recent value
        sav_length = len(sensor_array.history)
        for i in range(sav_length):
            if i > sav_length - 1:
                break
            current_sav = sensor_array.history[sav_length - (i + 1)]
            cooldown_factor = (now - current_sav.time) * cooldown
            if cooldown_factor == 0:
                # prevent div by 0
                cooldown_factor = 1
            if Line.is_something(current_sav):
                trend_array.append([(Line.get_bar_position(current_sav) - 2), cooldown_factor])
            else:
                for k in range(i + 1, sav_length):
                    current_sav = sensor_array.history[sav_length - (k + 1)]
                    if Line.is_something(current_sav):
                        trend_array.append([(Line.get_bar_position(current_sav) - 2), cooldown_factor])
                        break

            if len(trend_array) == values:
                break
        trend = 0
        if len(trend_array) < 2:
            return 0  # not enough values collected to calculate a trend
        for trend_id in range(1, len(trend_array)):
            # links < rechts            ((t-1) - (t)) / cooldown(t)
            trend += ((trend_array[trend_id][0] - trend_array[trend_id - 1][0]) / trend_array[trend_id][1])
        return trend

    def average_line_position(sensor_array: SensorArray, max_look_back_sec=2) -> float:
        """return the average line position of the last x seconds. returns 0..4"""
        now = time.monotonic()
        ctr = 0
        sum = 0
        for sav in reversed(sensor_array.history):
            if now - sav.time > max_look_back_sec:
                break  # stop analyzing if time target is reached
            if Line.get_bar_position(sav) == -0.5 or Line.get_bar_count(sav) > 1 or Line.get_bar_width(sav) > 2: # do not use undefined patterns
                continue
            ctr += 1
            sum += Line.get_bar_position(sav)
        if ctr == 0:
            return 2
        return sum / ctr
    
    def compress_line_by_time(sensor_array: SensorArray, seconds: float) -> SensorArrayValue:
        """Return all recorded sensor values of the last x seconds in one value"""
        now = time.monotonic()
        sav_return = SensorArrayValue([
            SensorValue(SensorValue.WHITE),
            SensorValue(SensorValue.WHITE),
            SensorValue(SensorValue.WHITE),
            SensorValue(SensorValue.WHITE),
            SensorValue(SensorValue.WHITE)
        ])
        for sav in reversed(sensor_array.history):
            if now - sav.time > seconds:
                break  # stop analyzing if time target is reached
            for x in range(SensorArray.LEFT_LEFT + 1):
                if sav[x] == SensorValue.BLACK:
                    sav_return[x] = SensorValue.BLACK
        return sav_return
