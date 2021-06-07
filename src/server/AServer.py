import asyncio
from asyncio import StreamReader, StreamWriter

from ClientHandler import ClientHandler


class AServer:

	clients: list[ClientHandler] = []
	port: int
	name: str = 'DefaultServer'
	motd: str = 'Welcome {username} to {servername}!'
	password: str = ''

	def __init__( self, port: int = 20307, websocket: bool = False ):
		self.port = port

	async def _handleClient(self, reader: StreamReader, writer: StreamWriter):
		self.clients.append( ClientHandler( self, reader, writer ) )

	async def _run_server(self):
		print( 'starting server' )
		self.server = await asyncio.start_server( self._handleClient, '0.0.0.0', self.port )
		async with self.server:
			print( 'server started' )
			print( f'listening on 0.0.0.0:{self.port}' )
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
