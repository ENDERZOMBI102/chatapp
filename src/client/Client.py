import socket
from typing import Callable, Optional, Union, Any
import threading
import logging
from data import Message

logger = logging.getLogger('CA-Client')


MessageListener = Callable[ [Message], None ]
CloseListener = Callable[ [], None ]


class Client:
	_socket: socket.socket
	_host: str = '127.0.0.1'
	_port: int = 20307
	_running: bool = False
	_messageCallback: MessageListener
	_closeCallback: CloseListener = lambda: None
	_rcvThread: Optional[threading.Thread] = None
	_calledOnClose: bool = False
	ignoreErrors: bool = True
	
	def SetAddress(self, host: str, port: Union[int, str] = 20307) -> None:
		logger.info(f'changing server to {host}:{port}!')
		self._host = host
		self._port = int(port)
		self._running = False
		if self._rcvThread:
			logger.info('stopping current connection...')
			self._socket.close()
			self._rcvThread.join()
		self._socket = socket.create_connection( (self._host, self._port) )
		self._run()
		logger.info('new connection created!')
	
	def SetUsername(self, uname: str) -> None:
		logger.info(f'changing username to {uname}')
		self.Send( Message( 'system', f':CHGUNAME:{uname}' ) )
	
	def GetAddress(self) -> str:
		return f'{self._host}:{self._port}'
	
	def SetMessageListener( self, func: MessageListener) -> None:
		self._messageCallback = func
		
	def SetCloseListener( self, func: CloseListener) -> None:
		self._closeCallback = func
	
	def Send( self, msg: Message ) -> None:
		if self._running:
			msgRaw: bytes = msg.toJson().encode()
			header = int.to_bytes( len(msgRaw), 4, 'big')
			self._socket.send(header)
			self._socket.send(msgRaw)
	
	def Stop(self) -> None:
		if self._running:
			self._running = False
			self._socket.close()
			self._rcvThread.join()
			self._rcvThread = None  # type: ignore
			self._onClose()
	
	def _onClose( self ) -> None:
		if not self._calledOnClose:
			self._closeCallback()
			self._calledOnClose = True
	
	def _run(self) -> None:
		self._running = True
		self._calledOnClose = False
		self._rcvThread = threading.Thread(target=self._rcv )
		self._rcvThread.start()
	
	def _rcv(self) -> None:
		while self._running:
			# noinspection PyBroadException
			try:
				raw_size = self._socket.recv(4)
			except Exception:
				if self.ignoreErrors:
					continue
				elif self._running:
					self._running = False
					self._onClose()
					raise
				else:
					return
			size = int.from_bytes(raw_size, 'big')
			if size == 0:
				continue
			logger.info(f'incoming message size: {size}')
			self._messageCallback(
				Message.fromJson(
					self._socket.recv(size).decode()  # decode() will from UTF-8 if no argument is given
				)
			)
	
	def __del__(self) -> None:
		self.Stop()
		
	def __enter__(self) -> 'Client':
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		self.Stop()
	
	@staticmethod
	def CheckIsValid( host: str, port: Union[int, str] ) -> bool:
		try:
			socket.getaddrinfo( host, port, 0, socket.SOCK_STREAM )
			return True
		except socket.gaierror:
			return False
