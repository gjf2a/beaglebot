# Simple GPIO library
from subprocess import call, check_output

def cmd_to(cmd, to):
    fout = open(to, "w")
    call(cmd.split(), stdout=fout)
    fout.close()

class GPIO_access(object):
    def __init__(self):
        self.gpio = {9:{12:60, 15:48, 23:49, 25:117, 27:115, 30:112, 41:20},
                     8:{7:66, 8:67, 9:69, 10:68, 11:45, 12:44, 14:26, 15:47,
                        16:46, 17:27, 18:65, 26:61}}
        self.gpio_path = "/sys/class/gpio/"
        self.live = {}

    def init_pin(self, board, pin):
        if not (board in self.gpio and pin in self.gpio[board]):
            raise NameError("Can't find " + str((board, pin)))
        code = str(self.gpio[board][pin])
        cmd_to("echo " + code, self.gpio_path + "export")
        self.live[code] = self.gpio_path + "gpio" + code + '/'
        self.set_dir(code, True)
        return code

    def check_gpio(self, gpio):
        if gpio not in self.live:
            raise NameError("Can't find " + gpio)        

    def set_dir(self, gpio, is_out):
        self.check_gpio(gpio)
        cmd_to("echo " + ("out" if is_out else "in"), self.live[gpio] + "direction")

    def set_value(self, gpio, value):
        self.check_gpio(gpio)
        cmd_to("echo " + str(value), self.live[gpio] + "value")
        
    def all_live(self):
        return [gpio for gpio in self.live]

    def kill_pin(self, gpio):
        self.check_gpio(gpio)
        cmd_to("echo " + gpio, self.gpio_path + "unexport")

    def shutdown_all(self):
        for code in self.live:
            self.kill_pin(code)
