import socket
from typing import Tuple
import socketserver as ss


class ReqHander(ss.StreamRequestHandler):

	request: socket.socket
	client_address: Tuple[str, int]
	Running: bool = True

	def handle(self):
		print(f'connection enstablished to "{self.client_address}"')
		self.server.clients[str(self.client_address)] = self
		while self.Running:
			try:
				raw_size = self.request.recv(64)
			except ConnectionResetError or ConnectionAbortedError:
				self.Running = False
				self.request.close()
				self.request.detach()
				del self.server.clients[str(self.client_address)]
				return
			size = int.from_bytes( raw_size, 'little' )
			msg = self.request.recv(size).decode()
			if msg in [' ', '']:
				continue
			print(f'[{self.client_address[0]}] received message: {msg}')
			self.server.send(msg=f'[{self.client_address[0]}] {msg}', sender=str( self.client_address) )

	def send(self, msg: bytes):
		if self.Running and self.request:
			header = int.to_bytes( len(msg), length=64, byteorder='little')
			self.request.send( header )
			self.request.send( msg )

