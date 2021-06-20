from browser import bind, document, websocket
from browser.widgets.dialog import InfoDialog, EntryDialog

from webtypes import MessageEvent


# noinspection PyStatementEffect
class Client:

	ws: websocket = None
	username: str = 'WebClient'

	def __init__( self ):
		if not websocket.supported:
			InfoDialog( "websocket", "WebSocket is not supported by your browser" )
			return

	def connect( self, ip: str ):
		# open a web socket
		self.ws = websocket.WebSocket( f'ws://{ip}' )
		# bind functions to web socket events
		self.ws.bind( 'open', self.OnOpen )
		self.ws.bind( 'message', self.OnMessage )
		self.ws.bind( 'close', self.OnClose )

	def OnOpen( self, evt ):
		document['sendbtn'].disabled = False
		self.Send( f':CHGUNAME:{self.username}' )

	@staticmethod
	def OnMessage( evt: MessageEvent ):
		# message received from server
		document['messages'] <= evt.data

	@staticmethod
	def OnClose( evt ):
		# websocket is closed
		document[ 'messages' ] <= f'[SYSTEM] Disconnected from server, code: {evt.code}'
		document['sendbtn'].disabled = True

	def Send( self, msg: str ):
		self.ws.send( msg )


client: Client = Client()


@bind('#sendbtn', 'click')
def send(evt):
	msg: str = document['msg'].value
	document['msg'].value = ''
	document['messages'] <= msg
	client.Send( msg )


@bind('#connbtn', 'click')
def connect(evt):
	diag = EntryDialog( 'Input server ip', 'The ip is in ADDRESS:PORT form' )

	@bind( diag, "entry" )
	def entry(evt):
		ip = diag.value
		diag.close()
		client.connect( ip )