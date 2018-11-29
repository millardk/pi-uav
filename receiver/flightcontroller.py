import Adafruit_PCA9685

class FlightController:

    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)

        self.servo_names = ['aileron', 'elevator', 'throttle', 'rudder', 'lflap', 'rflap']
        self.servo_minimums = [205,205,205,205,205,205]
        self.servo_maximums = [410,410,410,410,410,410]
        self.servo_reversed = [False, False, False, False, False, True]
        self.servo_failsafes = [0.5, 0.5, 0, 0.5, 0, 0]
        self.inputs = self.servo_failsafes.copy()
        self.last_output = [-1,-1,-1,-1,-1,-1]
        self.ap_mode = 0


    def update_inputs(self, xbee_message):        
        for x in range(4):
            self.inputs[x] = int(xbee_message.data[x]) / 255
            flaps = int((xbee_message.data[4] >> 6 & 3)) / 3;
        self.inputs[4] = flaps
        self.inputs[5] = flaps
        self.ap_mode = xbee_message.data[4] >> 5 & 1;
        

    def map_val(self, channel, setting):
        magnitude = (self.servo_maximums[channel] - self.servo_minimums[channel]) * setting
        output = 0
        if self.servo_reversed[channel]:
            output = self.servo_maximums[channel] - magnitude
        else:
            output = self.servo_minimums[channel] + magnitude
        return int(output)

    def do_control(self):
        for x in range(6):
            output = self.map_val(x, self.inputs[x])
            if output != self.last_output[x]:
                self.pwm.set_pwm(x, 0, output)

