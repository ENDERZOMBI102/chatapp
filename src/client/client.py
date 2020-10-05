import socket
from typing import Tuple
import threading


class Client:
    
    socket: socket.socket
    ADDR: str = '127.0.0.1'
    PORT: int = 20307
    Running: bool = True

    def __init__(self, ADDR: Tuple[str, int] = None ):
        if ADDR:
            self.ADDR, self.PORT = ADDR
        self.socket = socket.create_connection( (self.ADDR, self.PORT))

    def run(self):
        rcvThread = threading.Thread(target=self.rcv)
        rcvThread.start()
        while True:
            txt = str( input('>') )
            if txt == ':exit':
                self.Running = False
                rcvThread.join()
                self.socket.close()
                exit()
            msg = txt.encode()
            header = int.to_bytes( len(msg), 64, 'little')
            self.socket.send( header )
            self.socket.send(msg)
            
    def rcv(self):
        while self.Running:
            raw_size = self.socket.recv(64)
            size = int.from_bytes( raw_size, 'little' )
            print( self.socket.recv(size).decode() )

if __name__ == '__main__':
    client = Client()
    client.run()