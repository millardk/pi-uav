from digi.xbee.devices import XBeeDevice
import pigpio
import threading
import time
import flightcontroller

last_received = 0
last_checked = 0


def main():

    try:    
        device = XBeeDevice("/dev/ttyAMA0", 9600)
        device.open()

        fc = FlightController()

        def data_receive_callback(xbee_message):
            global last_received
            last_received = xbee_message.timestamp
            fc.update_inputs(xbee_message)
            fc.do_control()

        device.add_data_received_callback(data_receive_callback)
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


def blink():
    pi = pigpio.pi()
    pi.set_mode(13, pigpio.OUTPUT)
    pi.set_mode(16, pigpio.OUTPUT)

    def check_connection():
        global last_received
        global last_checked
        connection = last_received != last_checked
        last_checked = last_received
        return connection

    while(True):
        if check_connection():
            pi.write(16, 1)
        else:
            pi.write(13, 1)
        time.sleep(0.5)
        pi.write(13, 0)
        pi.write(16, 0)
        time.sleep(1.5)


if __name__ == '__main__':
    t = threading.Thread(target=blink)
    t.start()
    main()