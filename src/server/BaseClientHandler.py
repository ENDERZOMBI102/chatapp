from abc import ABCMeta, abstractmethod
from datetime import datetime
from time import time

from data import Message


class BaseClientHandler(metaclass=ABCMeta):

	alive: bool = True
	addr: str
	# noinspection PyUnresolvedReferences
	server: 'AServer'
	username: str = 'unregistered'

	# noinspection PyUnresolvedReferences
	def __init__(self, server: 'AServer', addr: str):
		self.server, self.addr = server, addr
		print( f'connection established to [{self.addr}]' )

	@abstractmethod
	async def Send( self, message: Message ) -> None:
		pass

	@abstractmethod
	async def InputLoop( self ) -> None:
		pass

	@abstractmethod
	async def CheckErrors( self ) -> None:
		pass

	async def ReplacePlaceholders( self, msg: Message ) -> Message:
		msg.content = (
			msg.content.replace( '{username}', self.username )
			.replace('{time}', datetime.now().strftime("%H:%M") )
			.replace('{servername}', self.server.name)
		)
		return msg

	async def HandleMessage( self, msg: Message ):
		print( f'[{self.addr}] {msg}' )
		# handle commands
		if msg.content.startswith( ':' ):
			await self.HandleCommand( msg )
		else:
			msg.content = f'[{self.username}] {msg.content}'
			await self.server.Broadcast( msg, self )

	async def HandleCommand( self, msg: Message ):
		cmd = msg.content.removeprefix( ':' ).split( ':' )
		if cmd[ 0 ] == 'CHGUNAME':
			oldname = self.username
			self.username = cmd[ 1 ]
			if oldname == 'unregistered':
				await self.server.Broadcast(
					msg=Message( 'system', f'{self.username} joined the server', time() ),
					sender=self
				)
				await self.Send( Message( 'system', f'joined "{self.server.name}"', time() ) )
				await self.Send( Message( 'system', f'MOTD:\n{self.server.motd}', time() ) )
			else:
				await self.server.Broadcast(
					msg=Message( 'system', f'{oldname} changed his name to {self.username}', time() ),
					sender=self
				)
				await self.Send( Message( 'system', 'changed name to {username}', time() ) )
		elif cmd[ 0 ] == 'SSERVER':
			raise KeyboardInterrupt
		else:
			await self.Send( Message( 'system', f'unknown command {cmd}', time() ) )
