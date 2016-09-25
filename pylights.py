#!/usr/bin/env python3
# vim:ts=4:sw=4:

import os.path as path

from configparser import ConfigParser

from pylights.pylights import PyLights

if __name__ == "__main__":
	cf=ConfigParser(allow_no_value=True)
	cf.read(path.join(path.dirname(path.realpath(__file__)), 'pylights.conf'))

	pl=PyLights(cf)

	pl.mainloop()
