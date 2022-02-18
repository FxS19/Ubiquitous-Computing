"""
Functions for driving
Board: Metro ESP32 S2 BETA
10.09.21 - group 1
"""

from line import Line
import time
from vehicle import Vehicle
from neopixel import NeoPixel
from sensor import Sensor, SensorValue
from sensorarray import SensorArrayValue, SensorArray
from recognizeShapes import RecognizeShapes
import drive_mode.race
import drive_mode.drive
from print import print_d
from line import Line

drive_modes = {
    "race": drive_mode.race.value,
    "drive": drive_mode.drive.value
}

class DriveByMatrix:
    """Functions for driving"""

    def __init__(self, mode: str, neopixel: NeoPixel) -> None:
        # Init Sensors
        self.sensor_array = SensorArray()

        # Init motors
        self.vehicle = Vehicle()
        self.__last_activated = time.monotonic()
        self.__alarm_sec = 0.05
        self.mode = mode
        self.neopixel = neopixel
        self.timer = 0

    def start(self):
        """Perform updates of the decissions of driving functions.
        This function does nothing if there are less then alarm_sec seconds since the last call"""
        while True:
            self.sensor_array.update(self.sens_update_callback)
            self.vehicle.update()
            if time.monotonic() - self.timer > self.__alarm_sec:
                self.neopixel[0] = (255, 0, 0)
            self.timer = time.monotonic()

            if self.__last_activated < time.monotonic() - self.__alarm_sec:
                self.hard_update()

    def hard_update(self):
        """Perform an update of the decissions of driving functions."""
        self.__last_activated = time.monotonic()
        current_sensor_value = self.sensor_array.history[-1]
        corner = RecognizeShapes.get_corner(self.sensor_array)

        if current_sensor_value == SensorValue.BLACK:
            #all black 90 degree to line
            self.__drive_mode_horizontal_line()
        elif corner:
            #drive recent corner
            self.__drive_mode_corner(corner)
            self.neopixel[0] = (0, 128, 0)
        elif current_sensor_value == SensorValue.WHITE:
            #Sensors complete white (end of line or line outside sensor array)
            self.__drive_mode_blind()
            self.neopixel[0] = (0, 0, 128)
        elif current_sensor_value != SensorValue.WHITE:
            #normal drive
            self.__drive_mode_normal(current_sensor_value)
            self.neopixel[0] = (0, 0, 0)
    
    def sens_update_callback(self, sav: SensorArrayValue):
        """Function that is called as callback when the sensor output has changed"""
        self.hard_update()
        corner = ""
        if RecognizeShapes.get_corner(self.sensor_array):
            corner = "corner"
        print_d("SENS:", sav, "{:.1f}".format(Line.get_bar_position(sav)), "\t", "{:.0f}".format(Line.get_bar_width(sav)), corner)

    def __drive_mode_normal(self, current_sensor_value):
        """Drive by the defined values"""
        max_speed = drive_modes[self.mode]["max_speed"]
        bar_width = Line.get_bar_width(current_sensor_value)
        bar_position = Line.get_bar_position(current_sensor_value)
        abs_bar_position = abs(bar_position - 2)
        speed = drive_modes[self.mode]["speed_table"][bar_width][int(abs_bar_position)]
        if int(bar_position) < 2:
            speed = tuple(reversed(speed))
        self.vehicle.set_speed(speed[0] * max_speed, speed[1] * max_speed)

    def __drive_mode_blind(self):
        """Sensors complete white (end of line or line outside sensor array)"""

        max_speed = drive_modes[self.mode]["max_speed"]
        last_valid_line_position = False
        for sensor_array in reversed(self.sensor_array.history):
            if Line.is_something(sensor_array) and Line.get_bar_position(sensor_array) != SensorArray.CENTER:
                last_valid_line_position = Line.get_bar_position(sensor_array)
                break
        if last_valid_line_position >= 0:
            if last_valid_line_position > SensorArray.CENTER:
                self.vehicle.set_speed(
                    drive_modes[self.mode]["outside_line_speed"][0] * max_speed,
                    drive_modes[self.mode]["outside_line_speed"][1] * max_speed)
            else:
                self.vehicle.set_speed(
                    drive_modes[self.mode]["outside_line_speed"][1] * max_speed,
                    drive_modes[self.mode]["outside_line_speed"][0] * max_speed)

    def __drive_mode_horizontal_line(self):
        """All sensors are black, in 90 degfrees to line -> something went wrong before"""
        speed_l = self.vehicle.motor_l.get_speed()
        speed_r = self.vehicle.motor_r.get_speed()
        if speed_l * 1.5 > speed_r and speed_r * 1.5 > speed_l:
            self.vehicle.set_speed(0, 0)
            print_d("Streight to line, can't yet decide!")
        else:
            if speed_l > speed_r:
                pass
                #self.vehicle.set_speed(-1 * MAX_SPEED, 1 * MAX_SPEED)
            else:
                pass
                #self.vehicle.set_speed(1 * MAX_SPEED, -1 * MAX_SPEED)

    def __drive_mode_corner(self, corner):
        """Drive around a corner -> two effective modes are available,
        speed defined in list above"""
        max_speed = drive_modes[self.mode]["max_speed"]
        bar_width = Line.get_bar_width(corner)
        bar_position = Line.get_bar_position(corner)
        abs_bar_position = abs(bar_position - 2)
        speed = drive_modes[self.mode]["speed_table"][bar_width][int(abs_bar_position)]
        if int(bar_position) < 2:
            speed = tuple(reversed(speed))
        self.vehicle.set_speed(speed[0] * max_speed, speed[1] * max_speed)
