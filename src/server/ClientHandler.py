import asyncio
import traceback
from asyncio import StreamWriter, StreamReader, Task

from .BaseClientHandler import BaseClientHandler
from data import Message


class ClientHandler(BaseClientHandler):

	_inputTask: Task
	_errorCheckTask: Task
	reader: StreamReader
	writer: StreamWriter

	# noinspection PyUnresolvedReferences
	def __init__( self, server: 'AServer', reader: StreamReader, writer: StreamWriter ):
		super().__init__( server, ':'.join( [ str(i) for i in writer.get_extra_info('peername') ] ) )
		self.reader = reader
		self.writer = writer
		print( f'[{self.addr}] getting client info' )
		# size = int.from_bytes( await self.reader.read( 64 ), 'little' )
		# msg = ( await self.reader.read( size ) ).decode( 'utf8' )
		print( f'[{self.addr}] starting input loop' )
		self._inputTask = asyncio.create_task( self.InputLoop() )
		self._errorCheckTask = asyncio.create_task( self.CheckErrors() )

	async def Send( self, message: Message ) -> None:
		if self.isAlive():
			message = await self.ReplacePlaceholders(message)
			enc_message = message.toJson().encode( 'utf8' )
			header = int.to_bytes( len( enc_message ), length=4, byteorder='big' )
			self.writer.write( header )
			self.writer.write( enc_message )
			await self.writer.drain()

	async def CheckErrors( self ) -> None:
		while True:
			await asyncio.sleep(10)
			exc: Exception = self.reader.exception()
			if exc is not None:
				if isinstance( exc, ConnectionResetError ):
					self._alive = False
					break
				print('Exception on reader:')
				traceback.print_exception( type( exc ), exc, exc.__traceback__ )

	async def InputLoop( self ) -> None:
		while (
				self.isAlive() and (
					self.reader.exception() is None or
					isinstance( self.reader.exception(), ConnectionResetError )
				)
		):
			size = int.from_bytes( await self.reader.read( 4 ), 'big' )
			msg = Message.fromJson(
				(
					await self.reader.read(size)
				).decode( 'utf8' )
			)
			await self.HandleMessage(msg)

		print( f'closed connection to [{self.addr}]' )
		self._alive = False
		
	def isAlive( self ) -> bool:
		return self._alive and not self.writer.is_closing()
