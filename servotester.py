import pigpio;
import curses
import time


pi = pigpio.pi();

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(True)


while(True):
    pi.set_servo_pulse(19,1500)

#
# while True:
#     c = stdscr.getch()
#     if c == curses.KEY_LEFT:
#
#
#     elif c == curses.KEY_RIGHT:
#
#     time.sleep(.033)