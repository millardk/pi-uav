from digi.xbee.devices import XBeeDevice
import Adafruit_PCA9685
import pigpio 
# TODO: Replace with the serial port where your local module is connected to. 

servo_min = 205
servo_max = 410
ledStatus=True

def map_value(val):
    range = servo_max - servo_min
    inc = range/256
    return int(servo_min + val*inc)

def main():
    def set_servo(channel, setting):
                output = map_value(setting)
                pwm.set_pwm(channel, 0, output)
                
    try:    
        device = XBeeDevice("/dev/ttyAMA0", 9600)
        device.open()
        
        pwm = Adafruit_PCA9685.PCA9685()
        pwm.set_pwm_freq(50)
        
        pi= pigpio.pi()
        pi.write(16,1)
       
        last = bytearray([0,0,0,0])
        for channel in range(4):
            set_servo(channel, last[channel])
        
        def data_receive_callback(xbee_message):
            global ledStatus
            if ledStatus:
                pi.write(16,0)
                ledStatus = False
            else:
                pi.write(16,1)
                ledStatus = True
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