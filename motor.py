#
# engine control
# Board: Metro ESP32 S2 BETA
# Adafruit DRV8871 Brushed DC Motor Driver
# 18.06.21 - wb
# v0.2
#

import board
import pulseio
import microcontroller
import math

class Motor:
    """Motor functions"""
    def __init__(self, io_pin_fwd: microcontroller.Pin, io_pin_bwd: microcontroller.Pin) -> None:
        fwd_pin = pulseio.PWMOut(io_pin_fwd)
        fwd_pin.duty_cycle = 0  # between 0 and 65535
        self.__fwd_pin = fwd_pin

        bwd_pin = pulseio.PWMOut(io_pin_bwd)
        bwd_pin.duty_cycle = 0  # between 0 and 65535
        self.__bwd_pin = bwd_pin

    def get_speed(self) -> int:
        if self.__fwd_pin.duty_cycle == 0:
            return self.__bwd_pin.duty_cycle
        return self.__fwd_pin.duty_cycle
    
    def set_speed(self, value: int) -> None:
        "value between -100 and 100"
        if value < 0:
            self.__fwd_pin.duty_cycle = 0
            self.__bwd_pin.duty_cycle = math.abs(value * 650) #reality between 0 and 65535 -> approximation
        elif value > 0:
            self.__fwd_pin.duty_cycle = value * 650 #reality between 0 and 65535 -> approximation
            self.__bwd_pin.duty_cycle = 0
        else:
            self.__fwd_pin.duty_cycle = 0
            self.__bwd_pin.duty_cycle = 0