
#simple http handler that turns on and off an led connected to the gpio

import http.server
import socketserver

import RPi.GPIO as GPIO

HOST = ""
PORT = 8081

class MyHTTPHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/LED_ON":
            GPIO.output(19, GPIO.HIGH)
            self.send_response(200)

        elif self.path == "/LED_OFF":
            GPIO.output(19, GPIO.LOW)
            self.send_response(200)

        else:
            self.send_response(404)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19,GPIO.OUT)

server = socketserver.TCPServer((HOST,PORT), MyHTTPHandler)
server.serve_forever()
