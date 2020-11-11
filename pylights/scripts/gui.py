# vim:ts=4:sw=4:

import os.path as path

from configparser import ConfigParser
from argparse import ArgumentParser

from pylights.pylights import PyLights

def run():
	parser = ArgumentParser(epilog='Command line options overrides the configuration file')
	parser.add_argument('-f', dest='filename', default='~/.pylights.conf', help='Load configuration from a file (defaults to ~/.pylights.conf)')

	parser.add_argument('-H', dest='host', help='SNMP host')
	parser.add_argument('-p', dest='port', help='SNMP port')
	parser.add_argument('-c', dest='context', help='SNMP context')
	parser.add_argument('-u', dest='username', help='SNMP user name')
#	parser.add_argument('-m', dest='mib', help='SNMP MIB root')

	parser.add_argument('-Apw', dest='auth_password', help='SNMP Authentication password')
	parser.add_argument('-Apr', dest='auth_protocol', help='SNMP Authentication protocol')
	parser.add_argument('-Ppw', dest='priv_password', help='SNMP Privacy password')
	parser.add_argument('-Ppr', dest='priv_protocol', help='SNMP Privacy protocol')

	args = parser.parse_args()

	cf = ConfigParser(allow_no_value=True)

	try:
		cf.read(path.expanduser(args.filename))
	except:
		cf.read_dict({'snmp': {}})

	for k,v in vars(args).items():
		if v:
			cf.set('snmp', k, v)

	pl=PyLights(cf)
	pl.mainloop()
