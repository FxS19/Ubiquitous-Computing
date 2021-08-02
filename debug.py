# Provide a basic playground
#
# from debug import *
import math
import board
from motor import Motor
from driver import Driver
from sensor import *

sensor_array = SensorArray([Sensor(board.IO9), Sensor(board.IO8), Sensor(board.IO7), Sensor(board.IO6), Sensor(board.IO5)])
driver = Driver(sensor_array, motor_l= Motor(io_pin_fwd= board.IO14, io_pin_bwd= board.IO13), motor_r= Motor(io_pin_fwd= board.IO15, io_pin_bwd= board.IO16), alarm_sec=0.1)