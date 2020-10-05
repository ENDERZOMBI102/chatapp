import socket
from typing import Tuple
import socketserver as ss


class ReqHander(ss.StreamRequestHandler):

	request: socket.socket
	client_address: Tuple[str, int]
	str_address: str
	Running: bool = True

	def handle(self):
		self.str_address = str( self.client_address )
		print(f'connection enstablished to [{self.client_address}]')
		self.server.clients[self.str_address] = self
		while self.Running:
			try:
				raw_size = self.request.recv(64)
			except ConnectionResetError or ConnectionAbortedError:
				self.Running = False
				self.request.close()
				self.request.detach()
				del self.server.clients[self.str_address]
				print(f'closed connection to [{self.client_address}]')
				return
			size = int.from_bytes( raw_size, 'little' )
			msg = self.request.recv(size).decode()
			if msg in [' ', '']:
				continue
			if msg.startswith(':'):
				cmd = msg.replace(':', '', 1).split(':')
				if cmd[0] == 'CHGUNAME':
					oldname = self.server.usernames[self.str_address]
					self.server.usernames[self.str_address] = cmd[1]
					self.server.send(msg=f'{oldname} changed his name to {cmd[1]}', sender=self.str_address)
					self.send( msg=f'changed name to {cmd[1]}'.encode() )
				if cmd[0] == 'SSERVER':
					raise KeyboardInterrupt
				continue
			print(f'[{self.client_address[0]}] received message: {msg}')
			self.server.send(msg=f'[{self.server.usernames[self.str_address]}] {msg}', sender=self.str_address )

	def send(self, msg: bytes):
		if self.Running and self.request:
			print(f'{self.client_address[0]}: sending')
			header = int.to_bytes( len(msg), length=64, byteorder='little')
			self.request.send( header )
			self.request.send( msg )

