from browser import bind, document, websocket
from browser.widgets.dialog import InfoDialog

def on_open(evt):
    document['sendbtn'].disabled = False

def on_message(evt):
    # message received from server
    document['messages'] <= evt.data

def on_close(evt):
    # websocket is closed
    document['sendbtn'].disabled = True

ws: websocket = None

def start(ev):
    if not websocket.supported:
        InfoDialog("websocket", "WebSocket is not supported by your browser")
        return
    global ws
    # open a web socket
    ws = websocket.WebSocket('https://20307-cada719f-7e1e-41c3-b740-01b962abb5a1.ws-eu01.gitpod.io')
    # bind functions to web socket events
    ws.bind('open',on_open)
    ws.bind('message',on_message)
    ws.bind('close',on_close)


def send(msg: str):
    global ws
    ws.send(msg)


@bind('#sendbtn', 'click')
def send(evt):
    msg: str = document['msg'].value
    document['msg'].value = ''
    document['messages'] <= msg
    send(msg)

start()
