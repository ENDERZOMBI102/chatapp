import socketserver as ss
import socket


class ReqHander(ss.StreamRequestHandler):
    def handle(self):
        print()




class Server(ss.ThreadingTCPServer, ss.TCPServer):
    """
    my socket server
    """
    PORT = 20307
    ADDR = socket.gethostbyname( socket.gethostname() )
    running: bool = True

    def __init__(self):
        super().__init__( (self.ADDR, self.PORT), ReqHander)
        print('starting server')
        print('server started')

    def listen(self):
        """
        start listening on ADDR:PORT
        """
        print(f'listening on {self.ADDR}:{self.PORT}')
        self.serve_forever()
        print('shutting down')
        self.server_close()
        self.running = False
        self.running = False

if __name__ == '__main__':
    with Server() as server:
        pass #reload?