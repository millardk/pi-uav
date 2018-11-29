from digi.xbee.devices import XBeeDevice
import Adafruit_PCA9685
import pigpio
import threading
import time
# TODO: Replace with the serial port where your local module is connected to. 

servo_min = 205
servo_max = 410

last_received = 0
last_checked = 0

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
       
        last = bytearray([0,0,0,0,0,0])
##        for channel in range(6):
##            set_servo(channel, last[channel])
        
        def data_receive_callback(xbee_message):
            global last_received
            last_received = xbee_message.timestamp
            for channel in range(4):
                if last[channel] != xbee_message.data[channel]:
                    set_servo(channel, xbee_message.data[channel])
                    last[channel] = xbee_message.data[channel]
                    
            flaps = xbee_message.data[4] >> 6 & 3;
            print(flaps)
            left_flap = 128-(flaps+1)*32
            if last[4] != left_flap:
                set_servo(4, left_flap)
                last[4] = left_flap
                
            right_flap = (flaps+1)*45-1
            if last[5] != right_flap:
                set_servo(5, right_flap)
                last[5] = right_flap
            
            ap_mode = xbee_message.data[4] >> 5 & 1;

        device.add_data_received_callback(data_receive_callback)
        print("Waiting for data...\n")
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