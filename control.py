from __future__ import print_function
from inputs import get_gamepad
from digi.xbee.devices import XBeeDevice
from time import sleep
import time

def scale_16_to_8(num):
    return num // 256


class ControlState:
    def __init__(self):
        self.aileron = 128
        self.elevator = 128
        self.throttle = 0
        self.rudder = 128

    def __repr__(self):
        return str(self.aileron) + " " + str(self.elevator) \
               + " " + str(self.throttle) + " " + str(self.rudder)

    def update(self):
        events = get_gamepad()
        diff = 2
        for event in events:
            if event.ev_type is "Absolute":
                if event.code is "ABS_RX":
                    temp = scale_16_to_8(event.state) + 128
                    if (temp < self.aileron - diff) | (temp > self.aileron + diff):
                        self.aileron = temp
                    # self.aileron = scale_16_to_8(event.state) + 128

                elif event.code is "ABS_RY":
                    temp = scale_16_to_8(event.state) + 128
                    if (temp < self.elevator - diff) | (temp > self.elevator + diff):
                        self.elevator = temp
                    # self.elevator = scale_16_to_8(event.state) + 128

                elif event.code is "ABS_Z":
                    temp = event.state
                    if temp < 20:
                        self.throttle = 0
                    elif (temp < self.throttle - diff) | (temp > self.throttle + diff):
                       self.throttle = temp
                    # self.throttle = event.state

                elif event.code is "ABS_X":
                    temp = scale_16_to_8(event.state) + 128
                    if (temp < self.rudder - diff) | (temp > self.rudder + diff):
                        self.rudder = temp
                    # self.rudder = scale_16_to_8(event.state) + 128

    def get_output(self):
        out = bytearray()
        out.append(255-self.aileron)
        out.append(self.elevator)
        out.append(self.throttle)
        out.append(255-self.rudder)
        return out


if __name__ == "__main__":
    PORT = "COM4"
    BAUD_RATE = 9600
    REMOTE_NODE_ID = "REMOTE"

    device = XBeeDevice(PORT, BAUD_RATE)
    device.open()
    xbee_network = device.get_network()
    remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
    if remote_device is None:
        print("Could not find the remote device")
        exit(1)

    cstate = ControlState()
    last = cstate.get_output()
    last_time = int(round(time.time() * 1000))

    while 1:
        cstate.update()
        output = cstate.get_output()
        # print(output)
        # print(cstate)
        now = int(round(time.time() * 1000))

        if ((output != last) & (now - last_time > 75)) | (last[2] != 0 and cstate.throttle == 0) | (abs(last[2] - cstate.throttle) > 10):
            last = output
            last_time = now
            # device.send_data(remote_device, output)
            device.send_data_async(remote_device, output)
            print(cstate)
        # sleep(1/15)
