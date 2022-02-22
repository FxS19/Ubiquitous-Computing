"""
Functions for driving
Board: Metro ESP32 S2 BETA
10.09.21 - group 1
"""
from time import time
from recognizeShapes import RecognizeShapes
from vehicle import Vehicle
from neopixel import NeoPixel
from sensor import SensorValue
from sensorarray import SensorArray
from line import Line

class Drive:
    __speed_values = {
        "base_speed": 25
    }

    def __init__(self, neopixel: NeoPixel, cubic_steer_aggressiveness: float, linear_steer_aggressiveness: float) -> None:
        self.neopixel = neopixel
        self.vehicle = Vehicle()
        self.active = True
        self.__normal_driving_mode = True
        self.__sensor_array = SensorArray()
        self.__cubic_steer_aggressiveness = cubic_steer_aggressiveness
        self.__linear_steer_aggressiveness = linear_steer_aggressiveness

    def start(self):
        """Start driving"""
        while self.active:
            self.__sensor_array.update(self.__sens_update_callback)
            self.vehicle.update()
            if self.__normal_driving_mode == True:
                # normal driving mode
                trend = RecognizeShapes.trend(self.__sensor_array, 3)
                #print_d("Trend:", trend)
                # limit trend values
                if trend > 4:
                    trend = 4
                    self.neopixel[0] = (128, 0, 90) # LED is pink, if trend is limited
                if trend < -4:
                    trend = -4
                    self.neopixel[0] = (128, 0, 90) # LED is pink, if trend is limited
                self.vehicle.motor_l.set_speed(self.__calc_normal_motor_speed(-trend) + ((Line.get_bar_position(self.__sensor_array.history[-1])-2) * 6))
                self.vehicle.motor_r.set_speed(self.__calc_normal_motor_speed(trend) - ((Line.get_bar_position(self.__sensor_array.history[-1])-2) * 6))
                self.__last_drive_mode = "normal"

            
    def __calc_normal_motor_speed(self, trend: float) -> float:
        return (trend * self.__cubic_steer_aggressiveness)**3 + (trend * self.__linear_steer_aggressiveness) + self.__speed_values["base_speed"] # tested with geogebra

    def __sens_update_callback(self, _):
        """Function that is called as callback when the sensor output has changed"""
        shape = RecognizeShapes.detect_corner_shape(self.__sensor_array, max_look_back_sec=0.8)
        current_sensor_value = self.__sensor_array.history[-1]

        if shape != '':
            # If a corner was detected and now there is no Line visible
            if shape[0] == '9': # about 90° corner detected
                if shape[1] == 'l':
                    self.vehicle.set_speed(self.__speed_values["base_speed"]/6, self.__speed_values["base_speed"])
                else:
                    self.vehicle.set_speed(self.__speed_values["base_speed"], self.__speed_values["base_speed"]/6)
            
            elif shape[0] == 'h': # robot is at an steep angle to the the corner
                if shape[1] == 'l':
                    self.vehicle.set_speed(-self.__speed_values["base_speed"]/2, self.__speed_values["base_speed"])
                else:
                    self.vehicle.set_speed(self.__speed_values["base_speed"], -self.__speed_values["base_speed"]/2)
            
            elif shape[0] == 't': # T crossing is visible
                if shape[1] == 'l': # no left turns
                    if RecognizeShapes.average_line_position(self.__sensor_array, 1) > Line.get_bar_position(current_sensor_value):
                        self.vehicle.set_speed(self.__speed_values["base_speed"]/3, self.__speed_values["base_speed"]/2)
                    else:
                        self.vehicle.set_speed(self.__speed_values["base_speed"]/2, self.__speed_values["base_speed"]/3)
                else: 
                    self.vehicle.set_speed(self.__speed_values["base_speed"], -self.__speed_values["base_speed"]/2)
        
        # If there is no line visible
        elif current_sensor_value == SensorValue.WHITE:
            self.__last_drive_mode = "blind"
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

        print("SENS:", current_sensor_value, "{:.1f}".format(Line.get_bar_position(current_sensor_value)), "\t", "{:.0f}".format(Line.get_bar_width(current_sensor_value)), self.__last_drive_mode, RecognizeShapes.detect_corner_shape(self.__sensor_array.history))
