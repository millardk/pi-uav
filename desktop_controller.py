import socket
import curses
import time

UDP_IP = "10.85.80.39"
UDP_PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

def send_led_on():
    sock.sendto(bytes("LED_ON", "utf-8"), (UDP_IP, UDP_PORT))

def send_led_off():
    sock.sendto(bytes("LED_OFF", "utf-8"), (UDP_IP, UDP_PORT))

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(True)

while True:
    c = stdscr.getch()
    if c == curses.KEY_LEFT:
        send_led_off()
    elif c == curses.KEY_RIGHT:
        send_led_on()

    time.sleep(.033)
