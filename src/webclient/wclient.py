from browser.websocket import WebSocket

from .. import data


connbtn = ...


class WebClient:
	ws: WebSocket
	username: str
	
	def Connect( self, ip: str ) -> None:
		self.ws = WebSocket(f'ws://{ip}')
		self.ws.bind( 'open', self.OnOpen )
		self.ws.bind( 'message', self.OnMessageRaw )
		self.ws.bind( 'error', self.OnError )
		self.ws.bind( 'close', self.OnClose )
	
	def OnOpen( self, evt ) -> None:
		connbtn.textContent = 'Disconnect'
	
	def OnMessageRaw( self, evt ) -> None:
		pass
	
	def OnError( self, evt ) -> None:
		pass
	
	def OnClose( self, evt ) -> None:
		pass
	
	
	
	
	