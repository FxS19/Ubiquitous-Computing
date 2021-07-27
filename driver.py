from sensor import SensorArray
from motor import Motor
import time

class Driver:
    """Functions for driving"""
    def __init__(self, sensor_array: SensorArray, motor_l: Motor, motor_r: Motor, alarm_sec: float) -> None:
        self.motor_l = motor_l
        self.motor_r = motor_r
        self.sensor_array = sensor_array
        self.__last_activated = time.monotonic()
        self.__alarm_sec = alarm_sec
    
    def do(self):
        """Driving function will only do something after at least self.__alarm_sec seconds"""
        if not self.__last_activated < time.monotonic() + self.__alarm_sec:
            return
        self.__alarm_sec = time.monotonic()
