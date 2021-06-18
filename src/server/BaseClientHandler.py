from abc import ABCMeta, abstractmethod


class BaseClientHandler(metaclass=ABCMeta):

	alive: bool = True
	addr: str
	server: 'AServer'
	username: str = 'unregistered'

	def __init__(self, server: 'AServer', addr: str):
		self.server, self.addr = server, addr
		print( f'connection established to [{self.addr}]' )

	@abstractmethod
	async def Send( self, message: str ) -> None:
		pass

	@abstractmethod
	async def InputLoop( self ) -> None:
		pass

	@abstractmethod
	async def CheckErrors( self ) -> None:
		pass

	async def HandleCommand( self, msg: str ):
		cmd = msg.removeprefix( ':' ).split( ':' )
		if cmd[ 0 ] == 'CHGUNAME':
			oldname = self.username
			self.username = cmd[ 1 ]
			if oldname == 'unregistered':
				await self.server.Broadcast(
					msg=f'{self.username} joined the server',
					sender=self
				)
				await self.Send( f'joined "{self.server.name}"' )
				await self.Send( f'MOTD:\n{self.server.motd}' )
			else:
				await self.server.Broadcast(
					msg=f'{oldname} changed his name to {self.username}',
					sender=self
				)
				await self.Send( 'changed name to {username}' )
		elif cmd[ 0 ] == 'SSERVER':
			raise KeyboardInterrupt
		else:
			await self.Send( f'unknown command {cmd}' )
