"""
Provide a basic playground

use:
from debug import *
to start
"""

import board
from motor import Motor, Vehicle
from driver import Driver
from sensor import SensorArray, Sensor

sensor_array = SensorArray([
    Sensor(board.IO9),
    Sensor(board.IO8),
    Sensor(board.IO7),
    Sensor(board.IO6),
    Sensor(board.IO5)])
vehicle = Vehicle(
    motor_l=Motor(io_pin_fwd=board.IO14, io_pin_bwd=board.IO13),
    motor_r=Motor(io_pin_fwd=board.IO15, io_pin_bwd=board.IO16))
driver = Driver(sensor_array, vehicle=vehicle, alarm_sec=0.05)

def start_update():
    """Perform sensor and motor updates in a loop"""
    while True:
        vehicle.update()
        sensor_array.update(print)

def update():
    """Perform sensor and motor updates"""
    vehicle.update()
    sensor_array.update(print)
