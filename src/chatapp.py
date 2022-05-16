from sys import argv

if '--server' in argv:
	if '--old' in argv:
		from server.server import Server

		Server()
	else:
		from server.AServer import AServer

		AServer( websocket='--websocket' in argv ).start()

elif '--bcli' in argv:
	from client import bcli

	bcli.App().MainLoop()
elif '--cli' in argv:
	from client import cli

	argv.remove('--cli')
	cli.main()
elif '--gui' in argv:
	from client import gui

	gui.App().MainLoop()
elif '--newcli' in argv:
	from client import newcli

	argv.remove('--newcli')
	newcli.main0()
elif '--android' in argv:
	from client.android import main

	argv.remove('--android')
	main.ChatApp().run()
elif '--t' in argv:
	from client import t
else:
	print('missing run type!')
	print('available:')
	for runType in ['android', 'bcli', 'cli', 'gui', 'newcli', 't', 'server', 'server --old']:
		print(f'\t--{runType}')
