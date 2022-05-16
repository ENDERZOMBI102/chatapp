import asyncio
from asyncio import StreamReader, StreamWriter
from typing import Union, Optional

import websockets
from websockets.legacy.server import Serve, WebSocketServerProtocol

from .BaseClientHandler import BaseClientHandler
from .ClientHandler import ClientHandler
from .WSClientHandler import WSClientHandler
from data import Message


class PlaceholderServer:
	def __init__( self ): ...
	async def __aenter__(self): ...
	async def __aexit__(self, exc_type, exc_val, exc_tb): ...


class AServer:
	_clients: list[BaseClientHandler] = []
	_useWS: bool
	_wsServer: Union[Serve, PlaceholderServer] = PlaceholderServer()
	_wsServerTask: Optional[asyncio.Task] = None
	_gcFuture: asyncio.Task
	_port: int
	_gcDelay: int = 30
	_name: str = 'DefaultServer'
	_motd: str = 'Welcome {username} to {servername}!'
	_password: str = ''
	
	def __init__( self, port: int = 20307, websocket: bool = False ):
		self._useWS = websocket
		self._port = port

	async def _startGarbageCollector( self ) -> None:
		while True:
			for client in self._clients:
				if not client.isAlive():
					self._clients.remove(client)
			await asyncio.sleep( self._gcDelay )
	
	async def _handleClient(self, reader: StreamReader, writer: StreamWriter):
		self._clients.append( ClientHandler( self, reader, writer ) )

	async def _handleWSClient( self, ws: WebSocketServerProtocol, uri: str ):
		handler = WSClientHandler( self, ws, uri )
		self._clients.append( handler )
		print( f'[{handler.addr}] starting input loop {uri}' )
		await handler.InputLoop()

	async def _run_server(self):
		print( 'starting server' )
		self._server = await asyncio.start_server( self._handleClient, '0.0.0.0', self._port )
		if self._useWS:
			self._wsServer = websockets.serve( self._handleWSClient, '0.0.0.0', self._port + 1 )
		self._gcFuture = asyncio.create_task( self._startGarbageCollector() )
		async with self._server, self._wsServer:
			print( 'server started' )
			print( f'{"sockets " if self._useWS else ""}listening on 0.0.0.0:{self._port}' )
			if self._useWS:
				print( f'websockets listening on 0.0.0.0:{self._port + 1}' )
			await self._server.serve_forever()

	async def broadcast( self, msg: Message, sender: ClientHandler ):
		for client in self._clients:
			if client.isAlive():
				if client is not sender:
					await client.Send(msg)
			else:
				print(f'Found closed client: {client.addr}')
				self._clients.remove(client)

	def start( self ):
		asyncio.run( self._run_server() )
	