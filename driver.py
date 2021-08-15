from sensor import SensorArray
from motor import Vehicle
from sensor import *
import time

MAX_SPEED = 35

class Driver:
    """Functions for driving"""
    timer = 0

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
        do_print =False
        if time.monotonic() - self.timer > 1:
            do_print = True
            self.timer = time.monotonic()

        result = 0 # Wert für links oder Rechts - -> links, + = rechts
        id_offset = 0
        for id, value in enumerate(reversed(self.sensor_array.history)):
            if value == SensorValue.WHITE: 
                id_offset += 1
                continue
            if do_print: print(id, str(value))
            row = 0
            for sv_id, sensorvalue in enumerate(value):
                if sensorvalue == SensorValue.BLACK:
                    row += sv_id - 2
            result += row/(id - id_offset + 1)
        
        if do_print:
            print("SETSPEED:", self.__calc_speed(-result), self.__calc_speed(result))
        self.vehicle.set_speed(self.__calc_speed(-result), self.__calc_speed(result))
        if do_print:
            print ("L/R", result)
            

    def __calc_speed(self, direction):
        MAX_VALUE = 5
        if direction < -MAX_VALUE: direction = -MAX_VALUE
        if direction > MAX_VALUE: direction = MAX_VALUE

        if direction < 0: 
            return MAX_SPEED
        else:
            return MAX_SPEED - MAX_SPEED * 2 * (1/(MAX_VALUE**2))*(direction**2)
            
