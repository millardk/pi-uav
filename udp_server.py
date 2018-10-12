import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        data = self.request[0].strip()
        print(data)
        
        
if __name__ == "__main__":
    HOST, PORT = "", 9999
    server = socketserver.UDPServer((HOST,PORT), MyUDPHandler)
    server.serve_forever()
    