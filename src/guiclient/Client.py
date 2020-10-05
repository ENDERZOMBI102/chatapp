import socket
from typing import Tuple, Callable
import threading


class Client:
	socket: socket.socket
	ADDR: str = '127.0.0.1'
	PORT: int = 20307
	Running: bool = True
	OnMessage: Callable[ [str], None ]

	def __init__(self, ADDR: Tuple[str, int] = None):
		if ADDR:
			self.ADDR, self.PORT = ADDR
		self.socket = socket.create_connection( (self.ADDR, self.PORT) )

	def SetAddress(self, host: int, port: int = 20307):
		self.ADDR = host
		self.PORT = port
		self.socket.close()
		self.socket = socket.create_connection( (self.ADDR, self.PORT) )

	def SetListener(self, func: Callable[ [str], None ]):
		self.OnMessage = func

	def Send(self, txt: str) -> None:
		msg: bytes = txt.encode()
		header = int.to_bytes(len(msg), 64, 'little')
		self.socket.send(header)
		self.socket.send(msg)

	def Run(self):
		rcvThread = threading.Thread(target=self.rcv)
		rcvThread.start()

	def rcv(self):
		while self.Running:
			raw_size = self.socket.recv(64)
			size = int.from_bytes(raw_size, 'little')
			Client.OnMessage( self.socket.recv(size).decode() )

	def __del__(self):
		self.socket.close()