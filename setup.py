from setuptools import setup, find_packages

setup(
	name = 'pylights',
	version = '1.0',
	packages = find_packages(),
	entry_points = {
		'console_scripts': [
			'pylights = pylights.scripts.gui:run'
		]
	},

	install_requires = [
		'easysnmp'
	],

	author = 'Staffan Thomen',
	author_email = 'staffan@thomen.fi',
	description = ('Control program for my SNMP lights system'),

	long_description = 'file:README.md',

	keywords = 'Custom SNMPv3 lights control',

	url = 'https://mercurial.shangtai.net/pylights',

	license = 'BSD',

	classifiers = [
		'Developmnt Status :: 4 - Beta',
		'Programming Language :: Python :: 3'
	]
)
