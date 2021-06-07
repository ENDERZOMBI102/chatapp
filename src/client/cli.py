import time
import optparse
import os

import Client

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
(options, args) = parser.parse_args()
options.username: str
options.address: str


# create client object
client: Client.Client = Client.Client()
# set listener function
client.SetListener( lambda msg: print(msg) )

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
			newname = txt.split(' ')[1]
			client.SetUsername(newname)
		# change server
		elif txt.startswith(':server '):
			host, port = txt.replace(':server ', '').split(':')
			client.SetAddress(host, port)
		# quit
		elif txt.startswith(':quit '):
			break
		continue
	client.Send(txt)

# destruct client
del client
