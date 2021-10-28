import time
import optparse
import os

from data import Message
from . import Client

parser = optparse.OptionParser()

parser.add_option(
	"--un",
	"--username",
	dest="username",
	type='string',
	help="use this username instead of the os username",
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


def main() -> None:
	options: Options = parser.parse_args()[0]  # type: ignore[assignment]

	# create client object
	client: Client.Client = Client.Client()
	# set listener function
	client.SetListener( lambda msg: print( msg.content ) )
	
	# set the server address
	host, port = options.address.split(':')
	client.SetAddress(host, port)
	
	# start the client
	client.Run()
	client.SetUsername( options.username )
	
	# event loop
	while True:
		time.sleep(0.01)
		txt = input()
	
		# commands
		if txt.startswith(':'):
			# change user name
			if txt.startswith(':name '):
				newName = txt.split(' ')[1]
				client.SetUsername(newName)
				options.username = newName
			# change server
			elif txt.startswith(':server '):
				host, port = txt.replace(':server ', '').split(':')
				client.SetAddress(host, port)
			# quit
			elif txt.startswith(':quit '):
				break
			continue
		client.Send( Message( options.username, txt, time.time() ) )
	
	# destruct client
	del client


if __name__ == '__main__':
	main()
