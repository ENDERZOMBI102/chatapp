import socketserver as ss
import socket
import threading
from typing import Dict, Tuple


class ReqHander(ss.StreamRequestHandler):

    request: socket.socket
    client_address: Tuple[str, int]

    def handle(self):
        print(f'connection enstablished to "{self.client_address}"')
        self.server.clients[str(self.client_address)] = self
        while True:
            raw_size = self.request.recv(64).decode()
            size = int ( raw_size )
            msg = self.request.recv(size).decode()
            print(f'[{self.client_address[0]}] recived message: {msg}')
            self.server.send(msg=f'[{self.client_address[0]}] {msg}', sender=str( self.client_address) )

    def send(self, msg: bytes):
        size = str( len(msg) )
        header = str( '0' * ( 64 - len( size ) ) + size )
        self.request.send( header.encode() )
        self.request.send( msg.decode().encode() )
        

class Server(ss.ThreadingTCPServer, ss.TCPServer):
    """
    my socket server
    """
    PORT = 20307
    ADDR = socket.gethostbyname( socket.gethostname() )
    running: bool = True
    clients: Dict[str,ReqHander] = {}

    def __init__(self):
        super().__init__( (self.ADDR, self.PORT), ReqHander)
        print('starting server')
        self.Thread = threading.Thread(target=self.serve_forever, daemon=True)
        self.Thread.start()
        print('server started')
        print(f'listening on {self.ADDR}:{self.PORT}')

    def send(self, msg:str, sender: str):
        raw_msg = msg.encode()
        for key, value in self.clients.items():
            if key == sender:
                continue
            value.send( msg=raw_msg )


if __name__ == '__main__':
    with Server() as server:
        while True:
            pass