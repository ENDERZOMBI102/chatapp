# noinspection PyUnresolvedReferences
from browser import bind, document, websocket
# noinspection PyUnresolvedReferences
from browser.widgets.dialog import InfoDialog, EntryDialog


class Client:

    ws: websocket = None

    def __init__( self ):
        if not websocket.supported:
            InfoDialog( "websocket", "WebSocket is not supported by your browser" )
            return

    def connect( self, ip: str ):
        # open a web socket
        self.ws = websocket.WebSocket( f'ws://{ip}' )
        # bind functions to web socket events
        self.ws.bind( 'open', self.on_open )
        self.ws.bind( 'message', self.on_message )
        self.ws.bind( 'close', self.on_close )

    def on_open(self, evt):
        document['sendbtn'].disabled = False

    def on_message(self, evt):
        # message received from server
        document['messages'] <= evt.data

    def on_close(self, evt):
        # websocket is closed
        document[ 'messages' ] <= f'[SYSTEM] Disconnected from server: {evt.__dict__}'
        document['sendbtn'].disabled = True

    def send(self, msg: str):
        self.ws.send(msg)


client: Client = Client()


@bind('#sendbtn', 'click')
def send(evt):
    msg: str = document['msg'].value
    document['msg'].value = ''
    document['messages'] <= msg
    client.send(msg)


@bind('#connbtn', 'click')
def send(evt):
    diag = EntryDialog( 'Input server ip', 'The ip is in ADDRESS:PORT form' )

    @bind( diag, "entry" )
    def entry( ev ):
        ip = diag.value
        diag.close()
        client.connect( ip )