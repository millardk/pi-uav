"""Simple example showing how to get gamepad events."""

from __future__ import print_function
from inputs import get_gamepad
from digi.xbee.devices import XBeeDevice


class ControlState:
    def __init__(self):
        self.lx = 0
        self.ly = 0
        self.rx = 0
        self.ry = 0

    def update(self):
        events = get_gamepad()
        for event in events:
            if event.ev_type is "Absolute":
                if event.ev_code is "ABS_X":
                    self.lx = event.state
                elif event.ev_code is "ABS_Y":
                    self.ly = event.state
                elif event.ev_code is "ABS_RX":
                    self.rx = event.state
                elif event.ev_code is "ABS_RY":
                    self.ry = event.state


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

    while 1:
        inputs = get_input()
        if inputs is not None:
            device.send_data(remote_device, inputs)