import curses
from curses import wrapper
from time import sleep

def main(stdscr):
    curses.cbreak()
    stdscr.keypad(True)
    
    pi = pigpio.pi()
    PIN = 18
    pi.set_mode(PIN, pigpio.OUTPUT)
    MIN = 1000
    MAX = 2000
    pulsewidth = 1500
    amt = 10

    while True:
        c = stdscr.getch()
        if c == curses.KEY_LEFT:
            pulsewidth -= amt;
            if pulsewidth < MIN:
                pulsewidth = MIN
            pi.set_servo_pulsewidth(PIN, pulsewidth)
            
        elif c == curses.KEY_RIGHT:
            pulsewidth += amt;
            if pulsewidth > MAX:
                pulsewidth = MAX
            pi.set_servo_pulsewidth(PIN, pulsewidth)

        sleep(1/60)
        
wrapper(main)
