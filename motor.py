"""
engine control
Board: Metro ESP32 S2 BETA
Adafruit DRV8871 Brushed DC Motor Driver
10.09.21 - group 1
v0.2
"""

import time
import math
import pwmio
import microcontroller

ACCELERATION = 250 # % per second
SPIKE_HEIGHT = 1.02#1.2

class Motor:
    """Motor functions"""
    __time_speed_start = 0
    __last = 0
    __target = 0
    __current_speed = 0

    def __init__(self, io_pin_fwd: microcontroller.Pin, io_pin_bwd: microcontroller.Pin) -> None:
        fwd_pin = pwmio.PWMOut(io_pin_fwd)
        fwd_pin.duty_cycle = 0  # between 0 and 65535
        self.__fwd_pin = fwd_pin

        bwd_pin = pwmio.PWMOut(io_pin_bwd)
        bwd_pin.duty_cycle = 0  # between 0 and 65535
        self.__bwd_pin = bwd_pin

    def get_speed(self) -> int:
        """Get the current speed of the motor. This is not the target speed!
        Due to the resolution of the pwm signal used for the motor,
        it is likely that the set motor value could be a bit less or higher"""
        return math.floor(self.__current_speed / 650)

    def set_speed(self, value: int) -> None:
        """Set the target speed of the motor, values from -100 to +100 are possible"""
        if self.__target == value:
            return
        self.__last = self.__estimate_speed(self.__last, self.__target)
        self.__time_speed_start = time.monotonic()
        self.__target = value
        delta = self.__target - self.__last
        self.set_speed_raw(math.floor(self.__target + delta * SPIKE_HEIGHT) * 650)

    def set_speed_raw(self, value: int) -> None:
        """Set the speed with +/-int16_t"""
        if value < 0:
            if value < -65535:
                value = -65535
            self.__current_speed = value
            self.__fwd_pin.duty_cycle = 0
            self.__bwd_pin.duty_cycle = -value #between 0 and 65535 -> approximation
        elif value > 0:
            if value > 65535:
                value = 65535
            self.__current_speed = value
            self.__fwd_pin.duty_cycle = value #between 0 and 65535 -> approximation
            self.__bwd_pin.duty_cycle = 0
        else:
            self.__current_speed = 0
            self.__fwd_pin.duty_cycle = 0
            self.__bwd_pin.duty_cycle = 0

    def mod_speed(self, value: int):
        """change the speed by a value between -100 and +100,
        if the result is outside 100% the maximum value is selected"""
        self.set_speed(self.get_speed() + value)

    def update(self):
        """Update the set speed and the target speed of the motor."""
        if (self.__target - self.get_speed()) == 0:
            return # do nothing if targetspeed is reached
        needed_time = abs(self.__target - self.__last) / ACCELERATION
        percentage = self.__get_current_runtime() / needed_time
        if percentage > 1:
            percentage = 1
        delta = self.__target - self.__last * 650
        self.set_speed_raw(math.floor(self.__target * 650 + delta * SPIKE_HEIGHT * (1-percentage)))

    def __estimate_speed(self, begin_speed, target_speed):
        """
        working with linear acceleration, could be imperfect
        TODO use degression
        """
        runtime = self.__get_current_runtime()
        if runtime * ACCELERATION + begin_speed < target_speed:
            return math.floor(begin_speed + runtime * ACCELERATION)
        return target_speed

    def __get_current_runtime(self):
        """Return the amount of that that passed since the last speed change"""
        return time.monotonic() - self.__time_speed_start
