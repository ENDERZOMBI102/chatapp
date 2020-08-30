import socket
from typing import Tuple
import threading


class Client:
    
    socket: socket.socket
    ADDR: str = socket.gethostbyname( socket.gethostname() )
    PORT: int = 20307

    def __init__(self, ADDR: Tuple[str, int] = None ):
        if ADDR:
            self.ADDR, self.PORT = ADDR
        self.socket = socket.create_connection( (self.ADDR, self.PORT))

    def run(self):
        rcvThread = threading.Thread(target=self.rcv)
        rcvThread.start()
        while True:
            msg = str( input('>') ).encode()
            size = str( len(msg) )
            header = str( '0' * ( 64 - len( size ) ) + size )
            self.socket.send( header.encode() )
            self.socket.send(msg)
            
    def rcv(self):
        while True:
            raw_size = self.socket.recv(64).decode()
            size = int( raw_size )
            print( self.socket.recv(size).decode() )

if __name__ == '__main__':
    client = Client()
    client.run()