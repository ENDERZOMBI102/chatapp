import socket
from typing import Tuple, Callable
import threading


class Client:

	socket: socket.socket
	ADDR: str = '127.0.0.1'
	PORT: int = 20307
	Running: bool = False
	OnMessage: Callable[ [str], None ]
	rcvThread: threading.Thread = None
	ignoreErrors: bool = True

	def __init__(self, ADDR: Tuple[str, int] = None):
		if ADDR:
			self.ADDR, self.PORT = ADDR
			self.socket = socket.create_connection( (self.ADDR, self.PORT) )

	def SetAddress(self, host: int, port: int = 20307):
		print(f'changing server to {host}:{port}!')
		self.ADDR = host
		self.PORT = port
		self.Running = False
		if self.rcvThread:
			print('stopping current connection...')
			self.socket.close()
			self.rcvThread.join()
		self.socket = socket.create_connection( (self.ADDR, self.PORT) )
		self.Run()
		print('new connection created!')

	def SetUsername(self, uname: str):
		print(f'changing username to {uname}')
		self.Send(f':CHGUNAME:{uname}')

	def GetAddress(self):
		return f'{self.ADDR}:{self.PORT}'

	def SetListener(self, func: Callable[ [str], None ]):
		self.OnMessage = func

	def Send(self, txt: str) -> None:
		msg: bytes = txt.encode()
		header = int.to_bytes(len(msg), 64, 'little')
		self.socket.send(header)
		self.socket.send(msg)

	def Stop(self):
		if self.Running:
			self.Running = False
			self.socket.close()
			self.rcvThread.join()

	def Run(self):
		self.Running = True
		self.rcvThread = threading.Thread(target=self.rcv)
		self.rcvThread.start()

	def rcv(self):
		while self.Running:
			try:
				raw_size = self.socket.recv(64)
			except:
				if self.ignoreErrors:
					continue
				elif self.Running:
					raise
				else:
					return
			size = int.from_bytes(raw_size, 'little')
			if size == 0:
				continue
			print(f'incoming message size: {size}')
			self.OnMessage( self.socket.recv(size).decode() )

	def __del__(self):
		self.Stop()