import Client
import optparse
import os

parser = optparse.OptionParser()

parser.add_option(
	"-un",
	"--username",
	dest="username",
	type='string',
	help="use this username instead of the os username",
	default=os.getlogin()
)

parser.add_option(
	"-ip",
	"--ip_address",
	dest="address",
	type='string',
	help="use this server instead of the default one, format: host:port",
	default='79.56.68.176:20307'
)
(options, args) = parser.parse_args()

