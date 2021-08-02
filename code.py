#
# Line following program
# Adafruit CircuitPython 6.2.0
# Board: Metro ESP32 S2 BETA
# Sensoren: KY-033 mit TCRT5000 (3x Digital)
# 28.06.21 - wb
# v0.2
#
import math
import board
from motor import Motor
from driver import Driver
from sensor import *

# SensorArray from left to right
sensor_array = SensorArray([Sensor(board.IO9), Sensor(board.IO8), Sensor(board.IO7), Sensor(board.IO6), Sensor(board.IO5)])
driver = Driver(sensor_array, motor_l= Motor(io_pin_fwd= board.IO14, io_pin_bwd= board.IO13), motor_r= Motor(io_pin_fwd= board.IO15, io_pin_bwd= board.IO16), alarm_sec=0.1)

max_speed = 30  # max speed (0-100)
counter = 0

while True:
    # choose direction
    sensor_array.update()
    if counter%1000==0: 
        print("left: " + str(driver.motor_l.get_speed()), "right: " + str(driver.motor_r.get_speed()))
    counter+=1

    # @TODO Aufgabe soll driver übernehmen
    if sensor_array.last_values[-1][SensorArray.CENTER] == SensorValue.BLACK:
        #print("driveForward")
        driver.motor_r.set_speed(max_speed)
        driver.motor_l.set_speed(max_speed)

    if sensor_array.last_values[-1][SensorArray.RIGHT] == SensorValue.BLACK:
        driver.motor_r.set_speed(max_speed) 
        driver.motor_l.set_speed(math.floor(0)) #max_speed/2

    if sensor_array.last_values[-1][SensorArray.RIGHT_RIGHT] == SensorValue.BLACK:
        #print("driveLeft")
        driver.motor_r.set_speed(max_speed)
        driver.motor_l.set_speed(-max_speed)
        
    if sensor_array.last_values[-1][SensorArray.LEFT]==SensorValue.BLACK:
        #print("driveRight")
        driver.motor_r.set_speed(math.floor(0)) #max_speed/2
        driver.motor_l.set_speed(max_speed)

    if sensor_array.last_values[-1][SensorArray.LEFT_LEFT] == SensorValue.BLACK:
        #print("driveLeft")
        driver.motor_r.set_speed(-max_speed)
        driver.motor_l.set_speed(max_speed)
    """    
    # if all Values are white the last Value should be used
    if sensor_array.all(SensorValue.WHITE):
        #print("driveLastDirection")
        if sensor_array.last_values[-1][SensorArray.CENTER] == SensorValue.BLACK:
            #print("driveForward")
            driver.motor_r.set_speed(max_speed)
            driver.motor_l.set_speed(max_speed)

        if sensor_array.last_values[-1](SensorArray.RIGHT) == SensorValue.BLACK:
            driver.motor_r.set_speed(max_speed) 
            driver.motor_l.set_speed(math.floor(0)) #max_speed/2

        if sensor_array.last_values[-1](SensorArray.RIGHT_RIGHT) == SensorValue.BLACK:
            #print("driveLeft")
            driver.motor_r.set_speed(max_speed)
            driver.motor_l.set_speed(-max_speed)
        
        if sensor_array.last_values[-1](SensorArray.LEFT)==SensorValue.BLACK:
            #print("driveRight")
            driver.motor_r.set_speed(math.floor(0)) #max_speed/2
            driver.motor_l.set_speed(max_speed)

        if sensor_array.last_values[-1](SensorArray.LEFT_LEFT) == SensorValue.BLACK:
            #print("driveLeft")
            driver.motor_r.set_speed(-max_speed)
            driver.motor_l.set_speed(max_speed)
"""