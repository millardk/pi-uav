import socketserver
import gpio_manager

class MyUDPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        data = self.request[0].strip()
        msg = data.decode("utf-8")

        if msg == "LED_ON":
            gpio_manager.led_on()
        elif msg == "LED_OFF":
            gpio_manager.led_off()

if __name__ == "__main__":
    HOST, PORT = "", 9999
    server = socketserver.UDPServer((HOST,PORT), MyUDPHandler)
    server.serve_forever()
    