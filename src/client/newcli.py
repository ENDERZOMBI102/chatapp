import curses
import optparse
import os
from queue import Queue

from data import Message
from .Client import Client


def main(scrn):
	curses.start_color()
	parser = optparse.OptionParser()

	parser.add_option(
		'--un',
		'--username',
		dest='username',
		type='string',
		help='use this username instead of os username',
		default=os.getlogin()
	)
	parser.add_option(
		'--ip',
		'--ip_address',
		dest='address',
		type='string',
		help='use this server instead of the default one, format: host:port',
		default='127.0.0.1:20307'
	)
	class Options:
		username: str
		address: str

	options, args = parser.parse_args()  # type: Options, list[str]

	inboundMessageQueue: Queue[ Message ] = Queue()
	line: int = 0

	client: Client = Client()
	client.SetListener( lambda msg: inboundMessageQueue.put(msg) )

	host, port = options.address.split(':')
	client.SetAddress(host, port)

	client.Run()
	client.SetUsername(options.username)

	scrn.addstr( 0, 0, f'Logged in as {options.username}' )
	# event loop
	try:
		scrn.nodelay(True)
		curses.nl()
		string = ''
		while True:
			c = scrn.getch()
			if 255 > c > -1:
				string += chr(c)
			
			if string.endswith('\n'):
				string = string[:-1]
				if string.startswith(':'):
					string = string[ 1: ]
					if string == 'q':
						break
				else:
					line += 1
					scrn.move( line, 0 )
					scrn.deleteln()
					scrn.addstr( line, 0, string )
					client.Send(string)
					string = ''
					
			for i in range( inboundMessageQueue.qsize() ):
				msg = inboundMessageQueue.get()
				line += 1
				scrn.addstr( line, 0, msg )
				inboundMessageQueue.task_done()
			
			scrn.move( line + 1, 0 )
			scrn.deleteln()
			scrn.addstr( line + 1, 0, '> ' + string )
	finally:
		del client


def main0() -> None:
	try:
		curses.wrapper(main)
	except Exception as e:
		print(e)
		input()


if __name__ == '__main__':
	main0()
