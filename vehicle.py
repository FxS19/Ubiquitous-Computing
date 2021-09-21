"""Combine motors to one vehicle"""

import board
from motor import Motor

class Vehicle:
    """combine two motors to a Vehicle"""
    def __init__(self) -> None:
        self.motor_l=Motor(io_pin_fwd=board.IO14, io_pin_bwd=board.IO13)
        self.motor_r=Motor(io_pin_fwd=board.IO15, io_pin_bwd=board.IO16)

    def update(self):
        """Update both motors"""
        self.motor_l.update()
        self.motor_r.update()

    def set_speed(self, left_speed, right_speed):
        """Set the target speed of the vehicle"""
        self.motor_l.set_speed(left_speed)
        self.motor_r.set_speed(right_speed)