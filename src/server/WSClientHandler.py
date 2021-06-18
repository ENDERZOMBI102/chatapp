from BaseClientHandler import BaseClientHandler


class WSClientHandler(BaseClientHandler):

	def __init__( self, server: 'AServer' ):
		super().__init__( server, None )

	async def Send( self, message: str ) -> None:
		pass

	async def InputLoop( self ) -> None:
		pass

	async def CheckErrors( self ) -> None:
		pass