import socket
from typing import Tuple


class client:
    
    socket: socket.socket
    ADDR: str = socket.gethostbyname( socket.gethostname() )
    PORT: int = 20307

    def __init__(self, ADDR: Tuple(str, int) = None ):
        if ADDR:
            self.ADDR, self.PORT = ADDR
        self.socket = socket.create_connection( (self.ADDR, self.PORT))
