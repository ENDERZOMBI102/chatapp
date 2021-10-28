import socket
from typing import Callable, Optional, Union
import threading
import logging
from data import Message

logger = logging.getLogger('CA-Client')


class Client:
	socket: socket.socket
	ADDR: str = '127.0.0.1'
	PORT: int = 20307
	Running: bool = False
	OnMessage: Callable[ [Message], None ]
	rcvThread: Optional[threading.Thread] = None
	ignoreErrors: bool = True

	def SetAddress(self, host: str, port: Union[int, str] = 20307):
		logger.info(f'changing server to {host}:{port}!')
		self.ADDR = host
		self.PORT = int(port)
		self.Running = False
		if self.rcvThread:
			logger.info('stopping current connection...')
			self.socket.close()
			self.rcvThread.join()
		self.socket = socket.create_connection( (self.ADDR, self.PORT) )
		self.Run()
		logger.info('new connection created!')

	# noinspection PyMethodMayBeStatic
	def CheckIsValid( self, host: str, port: Union[int, str] ) -> bool:
		try:
			socket.getaddrinfo( host, port, 0, socket.SOCK_STREAM )
			return True
		except socket.gaierror:
			return False

	def SetUsername(self, uname: str):
		logger.info(f'changing username to {uname}')
		self.Send( Message( 'system', f':CHGUNAME:{uname}' ) )

	def GetAddress(self):
		return f'{self.ADDR}:{self.PORT}'

	def SetListener(self, func: Callable[ [Message], None ]):
		self.OnMessage = func  # type: ignore[assignment, misc]

	def Send( self, msg: Message ) -> None:
		msgRaw: bytes = msg.toJson().encode()
		header = int.to_bytes( len(msgRaw), 64, 'little')
		self.socket.send(header)
		self.socket.send(msgRaw)

	def Stop(self):
		if self.Running:
			self.Running = False
			self.socket.close()
			self.rcvThread.join()
			self.rcvThread = None  # type: ignore

	def Run(self):
		self.Running = True
		self.rcvThread = threading.Thread(target=self.rcv)
		self.rcvThread.start()

	def rcv(self):
		while self.Running:
			# noinspection PyBroadException
			try:
				raw_size = self.socket.recv(64)
			except:
				if self.ignoreErrors:
					continue
				elif self.Running:
					self.Running = False
					raise
				else:
					return
			size = int.from_bytes(raw_size, 'little')
			if size == 0:
				continue
			logger.info(f'incoming message size: {size}')
			self.OnMessage( Message.fromJson( self.socket.recv(size).decode() ) )

	def __del__(self):
		self.Stop()
