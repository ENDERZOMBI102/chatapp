import importlib.util
import server
import hashlib
import asyncio
import threading


with open('./server.py', 'rb') as file:
    previusHash = hashlib.sha256( file.read() )

def hasChanged() -> bool:
    global previusHash
    with open('./server.py', 'rb') as file:
        newHash = hashlib.sha256( file.read() )
    if previusHash != newHash:
        print('yes')
        previusHash = newHash
        return True
    print('no')
    return False

def start() -> bool:
    srv = server.Server()
    thread = threading.Thread( target=srv.listen )
    thread.run()
    while True:
        print('hello')
        if hasChanged():
            print('reloading')
            thread._stop()
            srv.shutdown()
            importlib.reload(server)
            return start()
        if not srv.running:
            return False           



if __name__ == '__main__':
    start()
