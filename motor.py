#
# Motoransteuerung - Robo - Test 1
# Board: Metro M4 Express
# Adafruit DRV8871 Brushed DC Motor Driver
# 18.06.21 - wb
# v0.2
#

import board
import pulseio

# Motor R
MotorR_In1 = pulseio.PWMOut(board.IO14)
MotorR_In1.duty_cycle = 0  # zwischen 0 und 65535

# Motor L
MotorL_In1 = pulseio.PWMOut(board.IO15)
MotorL_In1.duty_cycle = 0  # zwischen 0 und 65535

def motorL(speed):  # linker Motor (Geschwindigkeit [0-100])
    mSpeed = speed * 650  # es werden Werte von 0-65535 benoetigt
    MotorL_In1.duty_cycle = mSpeed

def motorR(speed):  # rechter Motor (Geschwindigkeit [0-100])
    mSpeed = speed * 650  # es werden Werte von 0-65535 benoetigt
    MotorR_In1.duty_cycle = mSpeed


