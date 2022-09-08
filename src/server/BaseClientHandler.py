from __future__ import annotations
from abc import ABCMeta, abstractmethod
from datetime import datetime
from time import time_ns
from typing import TYPE_CHECKING

from data import Message

if TYPE_CHECKING:
	from Server import AServer


class BaseClientHandler(metaclass=ABCMeta):
	_alive: bool = True
	addr: str
	# noinspection PyUnresolvedReferences
	server: AServer
	username: str = 'unregistered'
	permissions: dict[ str, bool ] = { 'shutdownServer': False }

	# noinspection PyUnresolvedReferences
	def __init__(self, server: AServer, addr: str):
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
	
	@abstractmethod
	def isAlive( self ) -> bool:
		pass
	
	async def ReplacePlaceholders( self, msg: Message ) -> Message:
		msg.content = msg.content.format(
			username=self.username,
			time=datetime.now().strftime("%H:%M"),
			servername=self.server.getName()
		)
		return msg

	async def HandleMessage( self, msg: Message ):
		print( f'[{self.addr}] -> {msg}' )
		# handle commands
		if msg.content.startswith( ':' ):
			await self.HandleCommand( msg )
		else:
			msg.content = f'[{self.username}] {msg.content}'
			await self.server.broadcast( msg, self )

	async def HandleCommand( self, msg: Message ):
		cmd = msg.content[1:].split( ':' )
		if cmd[ 0 ] == 'CHGUNAME':
			oldname = self.username
			self.username = cmd[ 1 ]
			if oldname == 'unregistered':
				await self.server.broadcast(
					msg=Message( 'system', f'{self.username} joined the server', time_ns() ),
					sender=self
				)
				await self.Send( Message( 'system', f'joined "{self.server.getName()}"', time_ns() ) )
				await self.Send( Message( 'system', f'MOTD:\n{self.server.getMotd()}', time_ns() ) )
			else:
				await self.server.broadcast(
					msg=Message( 'system', f'{oldname} changed his name to {self.username}', time_ns() ),
					sender=self
				)
				await self.Send( Message( 'system', 'changed name to {username}', time_ns() ) )
		elif cmd[ 0 ] == 'SSERVER':
			if self.permissions['shutdownServer']:
				raise KeyboardInterrupt
			else:
				await self.Send( Message( 'system', 'i\'m afraid i cannot do that, {username}.', time_ns() ) )
		else:
			await self.Send( Message( 'system', f'unknown command {cmd}', time_ns() ) )
