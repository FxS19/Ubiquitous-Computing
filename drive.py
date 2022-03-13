"""
Functions for driving
Board: Metro ESP32 S2 BETA
10.09.21 - group 1
"""
import time
from recognizeShapes import RecognizeShapes
from vehicle import Vehicle
from neopixel import NeoPixel
from sensor import SensorValue
from sensorarray import SensorArray
from line import Line
from settingStorage import SettingStorage
import board
import digitalio

e = 2.7182818  # euler's number
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


class Drive:
    __speed_values = {
        "base_speed": 25
    }

    def __init__(self, neopixel: NeoPixel) -> None:
        self.neopixel = neopixel
        self.vehicle = Vehicle()
        self.active = True
        self.__normal_driving_mode = True
        self.__sensor_array = SensorArray()
        self.__cubic_steer_aggressiveness = float(SettingStorage.get_value("cubic_aggressiveness"))
        self.__linear_steer_aggressiveness = float(SettingStorage.get_value("linear_aggressiveness"))
        self.__corner_9_short_modifier = float(SettingStorage.get_value("corner_9_short_modifier"))
        self.__corner_9_long_modifier = float(SettingStorage.get_value("corner_9_long_modifier"))
        self.__corner_h_short_modifier = float(SettingStorage.get_value("corner_h_short_modifier"))
        self.__corner_h_long_modifier = float(SettingStorage.get_value("corner_h_long_modifier"))

    def start(self):
        """Start driving"""
        ctr = 0
        while self.active:
            self.__sensor_array.update(self.special_driving_modes)
            if ctr % 10 == 0:
                self.special_driving_modes(None)
            ctr += 1
            self.vehicle.update()
            led.value = not led.value

            if self.__normal_driving_mode is True:
                # normal driving mode
                trend = RecognizeShapes.trend(self.__sensor_array, 3)
                current_sensor_value = self.__sensor_array.history[-1]
                sig_modifier = 1 + 1 / (1 + e**(-(time.monotonic() - current_sensor_value.time) + 3)) # sigmoid function skaled, that the maximum amount is reached after one second
                line_position_modifier = (Line.get_bar_position(current_sensor_value) - 2) * 8 * sig_modifier

                # limit trend values
                if trend > 4:
                    trend = 4
                    self.neopixel[0] = (128, 0, 90)  # LED is pink, if trend is limited
                if trend < -4:
                    trend = -4
                    self.neopixel[0] = (128, 0, 90)  # LED is pink, if trend is limited

                self.vehicle.motor_l.set_speed(self.__calc_normal_motor_speed(-trend) + line_position_modifier)
                self.vehicle.motor_r.set_speed(self.__calc_normal_motor_speed(trend) - line_position_modifier)

    def __calc_normal_motor_speed(self, trend: float) -> float:
        return (trend * self.__cubic_steer_aggressiveness)**3 + (trend * self.__linear_steer_aggressiveness) + self.__speed_values["base_speed"]  # math tested with geogebra

    def special_driving_modes(self, _):
        """Detect end perform special driving tasks"""
        shape = RecognizeShapes.detect_corner_shape(self.__sensor_array, max_look_back_sec=0.8)
        current_sensor_value = self.__sensor_array.history[-1]

        if shape != '':
            # If a corner was detected and now there is no Line visible
            self.__normal_driving_mode = False
            if shape[0] == '9':  # about 90° corner detected
                self.neopixel[0] = (30, 0, 0)
                begin_time = time.monotonic()
                while (time.monotonic() < begin_time + 0.4): # drive some time over the edge but keep values up to date
                    self.__sensor_array.update() 
                    self.vehicle.update()
                if shape[1] == 'l':
                    self.vehicle.set_speed(
                        self.__speed_values["base_speed"] * self.__corner_9_short_modifier,
                        self.__speed_values["base_speed"] * self.__corner_9_long_modifier)
                else:
                    self.vehicle.set_speed(
                        self.__speed_values["base_speed"] * self.__corner_9_long_modifier,
                        self.__speed_values["base_speed"] * self.__corner_9_short_modifier)
                while (not Line.is_something(self.__sensor_array.history[-1])): # now there should not be any line visible. continue rotating until Line is visible
                    self.__sensor_array.update() 
                    self.vehicle.update()

            elif shape[0] == 'h':  # robot is at an steep angle to the the corner
                self.neopixel[0] = (255, 0, 0)
                if shape[1] == 'l':
                    self.vehicle.set_speed(
                        self.__speed_values["base_speed"] * self.__corner_h_short_modifier,
                        self.__speed_values["base_speed"] * self.__corner_h_long_modifier)
                else:
                    self.vehicle.set_speed(
                        self.__speed_values["base_speed"] * self.__corner_h_long_modifier,
                        self.__speed_values["base_speed"] * self.__corner_h_short_modifier)

            elif shape[0] == 't':  # T crossing is visible
                if shape[1] == 'l':  # do not turn left
                    self.neopixel[0] = (0, 0, 128)
                    self.vehicle.set_speed(0, 0)
                else:
                    self.neopixel[0] = (0, 0, 255)
                    self.vehicle.set_speed(self.__speed_values["base_speed"] * self.__corner_9_long_modifier, self.__speed_values["base_speed"] * self.__corner_9_short_modifier)
                    while (self.__sensor_array.history[-1][SensorArray.RIGHT_RIGHT] == SensorValue.WHITE): # rotate until line is visible on the right
                        self.__sensor_array.update() 
                        self.vehicle.update()

        # If there is no line visible
        elif current_sensor_value == SensorValue.WHITE:
            self.neopixel[0] = (128, 128, 128)
            self.__normal_driving_mode = False
            last_valid_line_position = False
            for sensor_array_value in reversed(self.__sensor_array.history):
                # search for the latest valid line position in the history
                if Line.is_something(sensor_array_value):
                    last_valid_line_position = Line.get_bar_position(sensor_array_value)
                    break
            if last_valid_line_position >= 0:
                if last_valid_line_position > SensorArray.CENTER:
                    # Line was valid on the right side
                    self.vehicle.set_speed(self.__speed_values["base_speed"], self.__speed_values["base_speed"] * -1)
                else:
                    # Line was valid on the left side or center
                    self.vehicle.set_speed(self.__speed_values["base_speed"] * -1, self.__speed_values["base_speed"])

        # normal driving mode
        else:
            self.__normal_driving_mode = True
            self.neopixel[0] = (0, 0, 0)

        # print("SENS:", current_sensor_value, "{:.1f}".format(Line.get_bar_position(current_sensor_value)), "\t", "{:.0f}".format(Line.get_bar_width(current_sensor_value)), RecognizeShapes.detect_corner_shape(self.__sensor_array))
