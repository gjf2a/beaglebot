#!/usr/bin/python3

from subprocess import call, check_output
from gpio import cmd_to
import os

ain = "AIN1"
motors = {"left_forward":66, "left_reverse":69, "right_forward":67, "right_reverse":68}
#motors = {"right_forward":67, "right_reverse":68}
min_safe = 1250
loops = 100

devs = {}
gpio = "/sys/class/gpio/"
ain_path = "/sys/devices/ocp.3/helper.15/" + ain

def main():
    init_motors()
    init_ir_debian()
    sense_action_loop(loops)
    shutdown_motors()

def set_motor(motor, value):
    cmd_to("echo " + str(value), devs[motor] + "value")

def init_motors():
    for motor in motors:
        pin = str(motors[motor])
        cmd_to("echo " + pin, gpio + "export")
        devs[motor] = gpio + "gpio" + pin + "/"
        cmd_to("echo out", devs[motor] + "direction")
    
# Debian 3.8.13
def init_ir_debian():
    cmd_to("echo cape-bone-iio", "/sys/devices/bone_capemgr.9/slots")

def sense_action_loop(counter):
    set_motor("left_forward", 1)

    while counter > 0:
        ir = int(check_output(["cat", ain_path]))
        info = "voltage: " + str(ir)
        if ir > min_safe:
            set_motor("right_reverse", 0)
            set_motor("right_forward", 1)
            info += ", Straight"
        else:
            set_motor("right_forward", 0)
            set_motor("right_reverse", 1)
            info += ", Turn"

        counter -= 1
        print(info, "(" + str(counter) + " to go)")

def shutdown_motors():
    for motor in motors:
        set_motor(motor, 0)
        cmd_to("echo " + str(motors[motor]), "/sys/class/gpio/unexport")

if __name__ == "__main__":
    main()
