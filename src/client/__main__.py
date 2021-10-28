from sys import argv


if '--bcli' in argv:
	from . import bcli
	bcli.App().MainLoop()
elif '--cli' in argv:
	from . import cli
	argv.remove('--cli')
	cli.main()
elif '--gui' in argv:
	from . import gui
	gui.App().MainLoop()
elif '--newcli' in argv:
	from . import newcli
	newcli.main0()
elif '--android' in argv:
	from .android import main
	main.ChatApp().run()
elif '--t' in argv:
	from . import t
else:
	print('missing client type!')
	print('available:')
	for client in ['android', 'bcli', 'cli', 'gui', 'newcli', 't']:
		print(f'\t--{client}')
