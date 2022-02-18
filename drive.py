"""
Functions for driving
Board: Metro ESP32 S2 BETA
10.09.21 - group 1
"""
from recognizeShapes import RecognizeShapes
from vehicle import Vehicle
from neopixel import NeoPixel
from sensor import SensorValue
from sensorarray import SensorArray
from line import Line

class Drive:
    __speed_values = {
        "max_speed": 25
    }

    def __init__(self, neopixel: NeoPixel) -> None:
        self.neopixel = neopixel
        self.vehicle = Vehicle()
        self.active = True
        self.__normal_driving_mode = True
        self.__sensor_array = SensorArray()
        self.__last_drive_mode = "normal"

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
        return (trend / 1.6)**3 + self.__speed_values["max_speed"] # tested with geogebra

    def __sens_update_callback(self, _):
        """Function that is called as callback when the sensor output has changed"""
        corner = RecognizeShapes.get_corner(self.__sensor_array, max_look_back_sec=4)
        current_sensor_value = self.__sensor_array.history[-1]
        
        # If a corner was detected and now there is no Line visible
        if corner:
            self.__last_drive_mode = "corner"
            self.neopixel[0] = (0, 0, 128)
            self.__normal_driving_mode = False
            if Line.get_bar_position(corner) < 2:
                # corner is on the left
                self.vehicle.set_speed(self.__speed_values["max_speed"]/6, self.__speed_values["max_speed"])
                #self.vehicle.set_speed(self.__speed_values["max_speed"] * -1, 0)# self.__speed_values["max_speed"]/2)
            else:
                # corner is on the right
                self.vehicle.set_speed(self.__speed_values["max_speed"], self.__speed_values["max_speed"]/6)
                #self.vehicle.set_speed(0, self.__speed_values["max_speed"] * -1)
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
                    self.vehicle.set_speed(self.__speed_values["max_speed"], self.__speed_values["max_speed"] * -1)
                else:
                    # Line was valid on the left side or center
                    self.vehicle.set_speed(self.__speed_values["max_speed"] * -1, self.__speed_values["max_speed"])
        else:
            self.__normal_driving_mode = True
            self.neopixel[0] = (0, 0, 0)

        print("SENS:", current_sensor_value, "{:.1f}".format(Line.get_bar_position(current_sensor_value)), "\t", "{:.0f}".format(Line.get_bar_width(current_sensor_value)), self.__last_drive_mode)
