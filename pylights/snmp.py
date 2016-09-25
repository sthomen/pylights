# vim:ts=4:sw=4:

from configparser import NoOptionError

from easysnmp import Session

class Snmp(object):
	config_section='snmp'

	def __init__(self, config):
		self.config=config

		params={
			'hostname': self.conf('host'),
			'remote_port': self.conf('port'),
			'version': 3,
			'use_numeric': True,						# required for OID matching
			'context': self.conf('context') or "",
			'security_username': self.conf('username'),
			'auth_protocol': self.conf('auth_protocol'),
			'auth_password': self.conf('auth_password'),
			'privacy_protocol': self.conf('priv_protocol'),
			'privacy_password': self.conf('priv_password')
		}

		# weed out unset values
		params={k: v for k,v in params.items() if v != None}

		if 'auth_protocol' in params.keys():
			params['security_level']='auth_without_privacy'
			if 'privacy_protocol' in params.keys():
				params['security_level']='auth_with_privacy'

		self.session=Session(**params)

	def conf(self, param):
		try:
			value=self.config.get(self.config_section, param)
		except NoOptionError:
			value=None

		return value

	def get(self, oid):
		return self.session.get(oid)

	def walk(self, oid):
		return self.session.walk(oid)

	def set(self, oid, value, snmp_type=None):
		return self.session.set(oid, value, snmp_type)
