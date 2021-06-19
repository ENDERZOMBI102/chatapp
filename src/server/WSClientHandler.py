import asyncio

from websockets.legacy.server import WebSocketServerProtocol

from BaseClientHandler import BaseClientHandler


class WSClientHandler(BaseClientHandler):

	wsocket: WebSocketServerProtocol
	uri: str
	_inputTask: asyncio.Task

	def __init__( self, server: 'AServer', ws: WebSocketServerProtocol, uri: str ):
		super().__init__( server, ws.remote_address )
		self.wsocket = ws
		self.uri = uri

		print( f'[{self.addr}] starting input loop' )
		self._inputTask = asyncio.create_task( self.InputLoop() )

	async def Send( self, message: str ) -> None:
		await self.wsocket.send( await self.ReplacePlaceholders( message )  )

	async def InputLoop( self ) -> None:
		while self.alive and not self.wsocket.closed:
			async for msg in self.wsocket:
				await self.HandleMessage(msg)
		self.alive = False

	async def CheckErrors( self ) -> None:
		pass