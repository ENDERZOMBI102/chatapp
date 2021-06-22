import asyncio

from websockets.exceptions import ConnectionClosedError
from websockets.legacy.server import WebSocketServerProtocol

from BaseClientHandler import BaseClientHandler


class WSClientHandler(BaseClientHandler):

	wsocket: WebSocketServerProtocol
	uri: str
	_inputTask: asyncio.Task

	def __init__( self, server: 'AServer', ws: WebSocketServerProtocol, uri: str ):
		super().__init__( server, ':'.join( [ str(i) for i in ws.remote_address ] ) )
		self.wsocket = ws
		self.uri = uri

	async def Send( self, message: str ) -> None:
		await self.wsocket.send( await self.ReplacePlaceholders( message )  )

	async def InputLoop( self ) -> None:
		try:
			while self.alive and not self.wsocket.closed:
				async for msg in self.wsocket:
					await self.HandleMessage(msg)
		except ConnectionClosedError:
			pass
		self.alive = False

	async def CheckErrors( self ) -> None:
		pass