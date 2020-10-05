import socketserver as ss
import socket
import threading
from typing import Dict, Tuple
from ReqHandler import ReqHander     

class Server(ss.ThreadingTCPServer, ss.TCPServer):
    """
    my socket server
    """
    PORT = 20307
    ADDR = '0.0.0.0'
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