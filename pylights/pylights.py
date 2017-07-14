# vim:ts=4:sw=4:

from tkinter import *
from collections import OrderedDict
from threading import Thread
from time import sleep

from .snmp import Snmp
from .device import Switch, Dimmer

class PyLights(Frame):

	mibroot='.1.3.6.1.4.1.8072.9999.9999.1.2'

	mib={
		'index':	'{}.1'.format(mibroot),
		'protocol':	'{}.2'.format(mibroot),
		'model':	'{}.3'.format(mibroot),
		'value':	'{}.4'.format(mibroot),
		'name':		'{}.5'.format(mibroot)
	}

	def __init__(self, config):
		self.config=config
		self.snmp=Snmp(self.config)
		self.widgets=[]

		root=Tk()
		root.title('PyLights')
		root.resizable(0,0)

		super().__init__(root)
		self.pack()

		self.updater=None
		self.update=BooleanVar(root, True)

		self.menu=Menu(self)
		filemenu=Menu(self.menu, tearoff=0)
		filemenu.add_command(label="Rescan devices", command=self.setup_devices)
		filemenu.add_checkbutton(label="Autorefresh dimmers", onvalue=True, offvalue=False, variable=self.update, command=self.toggle_update)
		filemenu.add_command(label="Quit", command=quit)
		
		self.menu.add_cascade(label="File", menu=filemenu)
		root.config(menu=self.menu)

		self.setup_devices()

	def setup_devices(self):
		for widget in self.widgets:
			widget.destroy()

		self.widgets=[]

		self.devices=self.load_devices()

		for device in self.devices.values():
			if 'dimmer' in device['model']:
				widget=Dimmer(self, title=device['name'])
				widget.setSetCallback(self.dim, [ device['index'] ])
				widget.setGetCallback(self.get, [ device['index'] ])
			else:
				widget=Switch(self, title=device['name'])
				widget.setSetCallback(self.set, [ device['index'] ])

			widget.set(device['value'])

			widget.pack()

			self.widgets.append(widget)

		if self.updater:
			self.updater.stop()

		self.updater=DimmerUpdateThread(self.widgets)
		self.updater.start()

	def load_devices(self):
		data=self.snmp.walk(self.mibroot)

		rmib=OrderedDict({v:k for k,v in self.mib.items()})

		devices=OrderedDict()

		for row in data:
			if not row.oid_index in devices:
				devices[row.oid_index]={}

			devices[row.oid_index][rmib[row.oid]]=row.value

		return devices

	def toggle_update(self):
		if self.update.get() == False:
			self.updater.pause()
		else:
			self.updater.resume()

	def get(self, index):
		result=self.snmp.get("{}.{}".format(self.mib['value'], index))
		return result.value

	def set(self, state, index):
		self.snmp.set("{}.{}".format(self.mib['value'], index), state, 'GAUGE')

	def dim(self, level, index):
		self.snmp.set("{}.{}".format(self.mib['value'], index), level, 'GAUGE')

class DimmerUpdateThread(Thread):
	def __init__(self, widgets):
		self.setWidgets(widgets)
		self.paused=False
		self.done=False

		super().__init__()

		self.daemon=True

	def setWidgets(self, widgets):
		self.widgets = widgets

	def waitLoop(self):
		sleep(1)

	def run(self):
		while not self.done:
			if not self.paused:
				for widget in self.widgets:
					if type(widget) == Dimmer:
						widget.get()

			self.waitLoop()

	def pause(self):
		self.paused=True

	def resume(self):
		self.paused=False

	def stop(self):
		self.done=True
