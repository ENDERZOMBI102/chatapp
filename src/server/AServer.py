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

	async def __aenter__(self):
		pass

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		pass


class AServer:

	clients: list[BaseClientHandler] = []
	useWS: bool
	wsServer: Union[Serve, PlaceholderServer] = PlaceholderServer()
	wsServerTask: Optional[asyncio.Task] = None
	port: int
	name: str = 'DefaultServer'
	motd: str = 'Welcome {username} to {servername}!'
	password: str = ''

	def __init__( self, port: int = 20307, websocket: bool = False ):
		self.useWS = websocket
		self.port = port

	async def _handleClient(self, reader: StreamReader, writer: StreamWriter):
		self.clients.append( ClientHandler( self, reader, writer ) )

	async def _handleWSClient( self, ws: WebSocketServerProtocol, uri: str ):
		handler = WSClientHandler( self, ws, uri )
		self.clients.append( handler )
		print( f'[{handler.addr}] starting input loop {uri}' )
		await handler.InputLoop()

	async def _run_server(self):
		print( 'starting server' )
		self.server = await asyncio.start_server( self._handleClient, '0.0.0.0', self.port )
		if self.useWS:
			self.wsServer = websockets.serve( self._handleWSClient, '0.0.0.0', self.port + 1 )
		async with self.server, self.wsServer:
			print( 'server started' )
			print( f'{"sockets " if self.useWS else ""}listening on 0.0.0.0:{self.port}' )
			if self.useWS:
				print( f'websockets listening on 0.0.0.0:{self.port + 1}' )
			await self.server.serve_forever()

	async def Broadcast( self, msg: Message, sender: ClientHandler ):
		for client in self.clients:
			if client.isAlive():
				if client is not sender:
					await client.Send(msg)
			else:
				print(f'Found closed client: {client.addr}')
				self.clients.remove(client)

	def Start( self ):
		asyncio.run( self._run_server() )
