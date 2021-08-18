from math import exp
from sensor import SensorArray
from motor import Vehicle
from sensor import *
import time

MAX_SPEED = 30

class Line:
    def is_something(array_value: SensorArrayValue):
        return array_value != SensorValue.WHITE

    def get_bar(array_value: SensorArrayValue):
        ctr = 0
        max = 0
        begin = 0
        begin_max = 0
        for id, sensor in enumerate(array_value):
            if sensor == SensorValue.BLACK:
                ctr+=1
                if ctr > max:
                    max = ctr
                    begin_max = begin
            else:
                ctr = 0
                begin = id + 1
        if max == 0: return (0,0)
        return (begin_max, max)

    def get_bar_width(array_value: SensorArrayValue):
        _ , max = Line.get_bar(array_value)
        return max

    def get_bar_position(array_value: SensorArrayValue):
        """return between 0 and 4"""
        begin_max , max_length = Line.get_bar(array_value)
        if max_length % 2 == 1:
            return begin_max + (max_length - 1) / 2.0
        return begin_max + max_length / 2.0 - 0.5
        

class Driver:
    """Functions for driving"""
    timer = 0
    speed_table = {
        # LL L C R RR
        # 2  1 0 1 2
        # left and right is swapped automatically

        #   0           1           2
        1: [(1, 1),     (0,1),      (-1,1)],    # Bar width: 1
        #   0,1         1,2
        2: [(0.7, 1),   (-0.3,1)],              # Bar width: 2
        #   1,0,1       0,1,2
        3: [(1, 1),     (-1,0)],                # Bar width: 3
        #   1,0,1,2
        4: [(-1,0)]                             # Bar width: 4
    }

    def __init__(self, sensor_array: SensorArray, vehicle: Vehicle, alarm_sec: float) -> None:
        self.vehicle = vehicle
        self.sensor_array = sensor_array
        self.__last_activated = time.monotonic()
        self.__alarm_sec = alarm_sec
    
    def update(self):
        """Driving function will only do something after at least self.__alarm_sec seconds"""
        if not self.__last_activated < time.monotonic() - self.__alarm_sec:
            return
        self.__last_activated = time.monotonic()
        do_print = False
        if time.monotonic() - self.timer > 1:
            do_print = True
            self.timer = time.monotonic()
        
        current_sensor_value = self.sensor_array.history[-1]

        #if do_print: #DEBUG
        #    print(
        #        "Bar center at: ", Line.get_bar_position(current_sensor_value), 
        #        " Bar width: ", Line.get_bar_width(current_sensor_value), 
        #        " RAW: ", Line.get_bar(current_sensor_value)
        #        )
        corner = self.get_corner()
        if corner:
            #drive recent corner
            bar_width = Line.get_bar_width(corner)
            bar_position = Line.get_bar_position(corner)
            abs_bar_position = abs(bar_position - 2)
            speed = self.speed_table[bar_width][int(abs_bar_position)]
            if int(bar_position) < 2:
                speed = tuple(reversed(speed))
            self.vehicle.set_speed(speed[1] * MAX_SPEED, speed[0] * MAX_SPEED) 
        elif current_sensor_value == SensorValue.BLACK:
            #all black
            speed_l = self.vehicle.motor_l.get_speed()
            speed_r = self.vehicle.motor_r.get_speed()
            if speed_l * 1.5 > speed_r and speed_r * 1.5 > speed_l:
                self.vehicle.set_speed(0,0)
                if do_print: print("Streight to line, can't yet decide!")
            else:
                if speed_l > speed_r:
                    pass
                    #self.vehicle.set_speed(-1 * MAX_SPEED, 1 * MAX_SPEED)
                else:
                    pass
                    #self.vehicle.set_speed(1 * MAX_SPEED, -1 * MAX_SPEED)
        elif current_sensor_value != SensorValue.WHITE:
            #normal drive
            bar_width = Line.get_bar_width(current_sensor_value)
            bar_position = Line.get_bar_position(current_sensor_value)
            abs_bar_position = abs(bar_position - 2)
            speed = self.speed_table[bar_width][int(abs_bar_position)]
            if int(bar_position) < 2:
                speed = tuple(reversed(speed))
            self.vehicle.set_speed(speed[1] * MAX_SPEED, speed[0] * MAX_SPEED)      
        elif current_sensor_value == SensorValue.WHITE:
            #Sensors complete white (end of line or between Sensors)
            return
            last_rev_id = 0
            last_valid_line = self.sensor_array.history[0]
            for id, sensor_array in enumerate(reversed(self.sensor_array.history)):
                if Line.is_something(sensor_array):
                    last_valid_line = sensor_array
                    last_rev_id = id
            position = Line.get_bar_position(sensor_array)
            if Line.is_bar(last_valid_line) or Line.is_between_sensor(last_valid_line):
                if position > 2:
                    self.vehicle.set_speed(MAX_SPEED, -MAX_SPEED)
                else:
                    self.vehicle.set_speed(-MAX_SPEED, MAX_SPEED)
        
    def get_corner(self):
        now = time.monotonic()
        MAX_LOOK_BACK_SEC = 1
        for sav in reversed(self.sensor_array.history):
            if now - sav.time > MAX_LOOK_BACK_SEC:
                return False
            width = Line.get_bar_width(sav)
            if width > 2 and width < 5:
                return sav
            return False
            
