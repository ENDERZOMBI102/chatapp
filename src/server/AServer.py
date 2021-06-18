import asyncio
from asyncio import StreamReader, StreamWriter

import websockets
from websockets.server import WebSocketServer

from BaseClientHandler import BaseClientHandler
from ClientHandler import ClientHandler
from WSClientHandler import WSClientHandler


class AServer:

	clients: list[BaseClientHandler] = []
	useWS: bool
	wsServer: WebSocketServer = None
	port: int
	name: str = 'DefaultServer'
	motd: str = 'Welcome {username} to {servername}!'
	password: str = ''

	def __init__( self, port: int = 20307, websocket: bool = False ):
		self.useWS = websocket
		self.port = port

	async def _handleClient(self, reader: StreamReader, writer: StreamWriter):
		self.clients.append( ClientHandler( self, reader, writer ) )

	async def _handleWSClient( self ):
		self.clients.append( WSClientHandler( self,  ) )

	async def _run_server(self):
		print( 'starting server' )
		self.server = await asyncio.start_server( self._handleClient, '0.0.0.0', self.port )
		async with self.server:
			print( 'server started' )
			print( f'{"sockets " if self.useWS else ""}listening on 0.0.0.0:{self.port}' )
			if self.useWS:
				self.wsServer = websockets.serve( self._handleWSClient, '0.0.0.0', self.port + 1 )
				self.wsServer
				print( f'websockets listening on 0.0.0.0:{self.port + 1}' )
			await self.server.serve_forever()

	async def Broadcast( self, msg: str, sender: ClientHandler ):
		for client in self.clients:
			if client.alive:
				if client is not sender:
					await client.Send(msg)
			else:
				self.clients.remove(client)

	def Start( self ):
		asyncio.run( self._run_server() )


AServer().Start()
