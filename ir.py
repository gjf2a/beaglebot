#!/usr/bin/python3

from subprocess import call, check_output
from sept_demo import init_ir_debian, cmd_to
import os

ain = "AIN1"
min_safe = 1250

ain_path = "/sys/devices/ocp.3/helper.15/" + ain

def main():
    init_ir_debian()
    sense_loop(1000)

def sense_loop(counter):
    while counter > 0:
        ir = int(check_output(["cat", ain_path]))
        info = "voltage: " + str(ir)
        counter -= 1
        print(info, "(" + str(counter) + " to go)")

if __name__ == "__main__":
    main()
