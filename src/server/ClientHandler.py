import asyncio
import traceback
from datetime import datetime
from asyncio import StreamWriter, StreamReader


class ClientHandler:

	_task: asyncio.Task
	alive: bool = True
	addr: str
	reader: StreamReader
	writer: StreamWriter
	server: 'AServer'
	username: str = 'unregistered'

	def __init__(self, server: 'AServer', reader: StreamReader, writer: StreamWriter):
		self.addr = writer.get_extra_info('peername')
		self.addr = f'{self.addr[0]}:{self.addr[1]}'
		print( f'connection established to [{self.addr}]' )
		self.server = server
		self.reader = reader
		self.writer = writer
		print( f'[{self.addr}] getting client info' )
		# size = int.from_bytes( await self.reader.read( 64 ), 'little' )
		# msg = ( await self.reader.read( size ) ).decode( 'utf8' )
		print( f'[{self.addr}] starting input loop' )
		self._inputTask = asyncio.create_task( self.InputLoop() )
		self._errorCheckTask = asyncio.create_task( self.CheckErrors() )

	async def Send( self, message: str ):
		message = message.replace( '{username}', self.username )\
			.replace('{time}', datetime.now().strftime("%H:%M") )
		enc_message = message.encode( 'utf8' )
		header = int.to_bytes( len( enc_message ), length=64, byteorder='little' )
		self.writer.write( header )
		self.writer.write( enc_message )
		await self.writer.drain()

	async def CheckErrors( self ):
		while True:
			await asyncio.sleep(10)
			exc: Exception = self.reader.exception()
			if exc is not None:
				print('Exception on reader:')
				traceback.print_exception( type( exc ), exc, exc.__traceback__ )

	async def InputLoop( self ):
		while not self.writer.is_closing():
			size = int.from_bytes( await self.reader.read( 64 ), 'little' )
			msg = ( await self.reader.read(size) ).decode( 'utf8' )
			print(f'[{self.addr}] {msg}')
			# handle commands
			if msg.startswith(':'):
				cmd = msg.removeprefix(':').split(':')
				if cmd[0] == 'CHGUNAME':
					oldname = self.username
					self.username = cmd[1]
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
				elif cmd[0] == 'SSERVER':
					raise KeyboardInterrupt
				else:
					await self.Send( f'unknown command {cmd}' )
			await self.server.Broadcast( f'[{self.username}] {msg}', self )

		print( f'closed connection to [{self.addr}]' )
		self.alive = False
