import socketserver as ss
import threading
from socket import socket
from typing import Dict

from .ReqHandler import ReqHandler


class Server(ss.ThreadingTCPServer, ss.TCPServer):
	"""
	my socket server
	"""
	PORT = 20307
	ADDR = '0.0.0.0'
	running: bool = True
	clients: Dict[str, ReqHandler] = {}
	usernames: Dict[str, str] = {}
	socket: socket

	def __init__(self):
		super().__init__( (self.ADDR, self.PORT), ReqHandler)
		print('starting server')
		self.Thread = threading.Thread(target=self.serve_forever, daemon=True)
		self.Thread.start()
		print('server started')
		print(f'listening on {self.ADDR}:{self.PORT}')

	def send(self, msg: str, sender: str):
		raw_msg = msg.encode()
		toRemove = []
		for key, value in self.clients.items():
			if key == sender:
				continue
			try:
				value.send( msg=raw_msg )
			except OSError:
				toRemove.append( key )
		for i in toRemove:
			del self.clients[i]


if __name__ == '__main__':
	with Server() as server:
		try:
			while True:
				pass
		except KeyboardInterrupt:
			server.server_close()
			server.socket.detach()
