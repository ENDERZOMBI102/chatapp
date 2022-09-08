import asyncio
from json import JSONDecodeError

from websockets.exceptions import ConnectionClosedError
from websockets.legacy.server import WebSocketServerProtocol

import util
from data import Message
from .BaseClientHandler import BaseClientHandler


class WSClientHandler(BaseClientHandler):

	wsocket: WebSocketServerProtocol
	uri: str
	_inputTask: asyncio.Task

	# noinspection PyUnresolvedReferences
	def __init__( self, server: 'AServer', ws: WebSocketServerProtocol, uri: str ):
		super().__init__( server, ':'.join( [ str(i) for i in ws.remote_address ] ) )
		self.wsocket = ws
		self.uri = uri

	async def Send( self, message: Message ) -> None:
		await self.wsocket.send(
			(
				await self.ReplacePlaceholders( message )
			).toJson()
		)

	async def InputLoop( self ) -> None:
		try:
			while self.isAlive():
				async for msg in self.wsocket:
					assert isinstance( msg, str ), 'got invalid message in bytes from web client, wtf?'
					try:
						await self.HandleMessage( Message.fromJson( msg ) )
					except JSONDecodeError as e:
						await self.wsocket.send( f'Expected JSON Message object, got {msg}: { util.getException(e) }' )
		except ConnectionClosedError as e:
			print('CCE:', e)
		self._alive = False

	async def CheckErrors( self ) -> None:
		pass
	
	def isAlive( self ) -> bool:
		return self._alive and not self.wsocket.closed
