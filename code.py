#
# Line following program
# Adafruit CircuitPython 6.2.0
# Board: Metro ESP32 S2 BETA
# Sensoren: KY-033 mit TCRT5000 (3x Digital)
# 28.06.21 - wb
# v0.2
#

import time
import math
import board
from motor import Motor
from driver import Driver
from sensor import *

# SensorArray from left to right
sensor_array = SensorArray([Sensor(board.IO5), Sensor(board.IO6), Sensor(board.IO7), Sensor(board.IO8), Sensor(board.IO9)])
driver = Driver(Motor(io_pin_fwd= board.IO14, io_pin_bwd= board.IO13), Motor(io_pin_fwd= board.IO15, io_pin_bwd= board.IO16), alarm_sec=0.1)

max_speed =100  # max speed (0-100)
counter = 0

while True:
    counter+=1
    driver.do()
    if counter%1000==0: print(str(sensor_array))
    # choose direction
    

    # @TODO Aufgabe soll driver übernehmen
    if sensor_array.read(SensorArray.CENTER) == SensorValue.BLACK:
        #print("driveForward")
        driver.motor_r.set_speed(max_speed)
        driver.motor_l.set_speed(max_speed)

    if sensor_array.read(SensorArray.LEFT) == SensorValue.BLACK:
        driver.motor_r.set_speed(max_speed)
        driver.motor_l.set_speed(math.floor(max_speed/2))

    if sensor_array.read(SensorArray.LEFT_LEFT) == SensorValue.BLACK:
        #print("driveLeft")
        driver.motor_r.set_speed(max_speed)
        driver.motor_l.set_speed(0)
        
    if sensor_array.read(SensorArray.RIGHT)==SensorValue.BLACK:
        #print("driveRight")
        driver.motor_r.set_speed(math.floor(max_speed/2))
        driver.motor_l.set_speed(max_speed)

    if sensor_array.read(SensorArray.RIGHT_RIGHT) == SensorValue.BLACK:
        #print("driveLeft")
        driver.motor_r.set_speed(0)
        driver.motor_l.set_speed(max_speed)
