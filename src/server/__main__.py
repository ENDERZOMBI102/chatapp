from sys import argv

from server.AServer import AServer


if '--old' in argv:
	from server.server import Server
	Server()
else:
	AServer( websocket='--websocket' in argv ).Start()
