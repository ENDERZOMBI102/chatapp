import curses
from curses import ascii
import optparse
import os
import traceback
from queue import Queue

from data import Message
from .Client import Client


class Options:
	username: str
	address: str


def main( scrn ):
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

	options, args = parser.parse_args()  # type: Options, list[str]

	inboundMessageQueue: Queue[ Message ] = Queue()
	line: int = 0

	with Client() as client:
		client.setMessageListener( inboundMessageQueue.put )

		host, port = options.address.split(':')
		client.setAddress( host, port )
		client.setUsername( options.username )

		scrn.addstr( 0, 0, f'[SYSTEM] Logged in as {options.username}' )
		# event loop
		scrn.nodelay(True)
		string = ''
		while True:
			c = scrn.getch()
			if 255 > c > -1:
				string += chr(c)
			if c == ascii.BS:
				string = string[:-2]

			if string.endswith('\n'):
				string = string[ :-1 ]
				if string.startswith(':'):
					string = string[ 1: ]
					if string == 'q':
						break
				else:
					line += 1
					scrn.move( line, 0 )
					scrn.deleteln()
					scrn.addstr( line, 0, string )
					client.send( string )
					string = ''

			for i in range( inboundMessageQueue.qsize() ):
				msg = inboundMessageQueue.get()
				line += 1
				scrn.addstr( line, 0, msg.content )
				inboundMessageQueue.task_done()

			scrn.move( line + 1, 0 )
			scrn.deleteln()
			scrn.addstr( line + 1, 0, '> ' + string )


def main0() -> None:
	try:
		curses.wrapper(main)
	except Exception as e:
		traceback.print_exception( type(e), e, e.__traceback__ )


if __name__ == '__main__':
	main0()
