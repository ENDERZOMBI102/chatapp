import socket
from typing import Tuple
import socketserver as ss

class ReqHander(ss.StreamRequestHandler):

    request: socket.socket
    client_address: Tuple[str, int]

    def handle(self):
        print(f'connection enstablished to "{self.client_address}"')
        self.server.clients[str(self.client_address)] = self
        while True:
            raw_size = self.request.recv(64)
            size = int.from_bytes( raw_size, 'little' )
            msg = self.request.recv(size).decode()
            print(f'[{self.client_address[0]}] recived message: {msg}')
            self.server.send(msg=f'[{self.client_address[0]}] {msg}', sender=str( self.client_address) )

    def send(self, msg: bytes):
        header = int.to_bytes( len(msg), length=64, byteorder='little')
        self.request.send( header )
        self.request.send( msg )
