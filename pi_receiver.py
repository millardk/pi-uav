import socketserver
import pigpio

def led_on():
    pi.write(19, 1)

def led_off():
    pi.write(19, 0)

class MyUDPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        data = self.request[0].strip()
        msg = data.decode("utf-8")

        if msg == "LED_ON":
            gpio_manager.led_on()
        elif msg == "LED_OFF":
            gpio_manager.led_off()

if __name__ == "__main__":
    pi = pigpio.pi()
    HOST, PORT = "", 9999
    server = socketserver.UDPServer((HOST,PORT), MyUDPHandler)
    server.serve_forever()
    