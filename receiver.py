from digi.xbee.devices import XBeeDevice
import Adafruit_PCA9685

# TODO: Replace with the serial port where your local module is connected to. 

servo_min = 205
servo_max = 410

def map_value(val):
    range = servo_max - servo_min
    inc = range/256
    return int(servo_min + val*inc)

def main():
    print(" +-----------------------------------------+")
    print(" | XBee Python Library Receive Data Sample |")
    print(" +-----------------------------------------+\n")

    device = XBeeDevice("/dev/ttyAMA0", 9600)
    pwm = Adafruit_PCA9685.PCA9685()
    pwm.set_pwm_freq(50)
    
    last = bytearray([0,0,0,0])
    
    def set_servo(channel, setting):
                output = map_value(setting)
                pwm.set_pwm(channel, 0, output)
                
    for channel in range(4):
        set_servo(channel, last[channel])

    try:
        device.open()
        
        def data_receive_callback(xbee_message):
##            print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
##                                     xbee_message.data))
            for channel in range(4):
                if last[channel] != xbee_message.data[channel]:
                    set_servo(channel, xbee_message.data[channel])
                    last[channel] = xbee_message.data[channel]

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()