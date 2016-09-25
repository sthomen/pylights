# vim:ts=4:sw=4:

from tkinter import *

from .snmp import Snmp

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
		super().__init__(Tk())
		self.pack()

		self.config=config
		self.snmp=Snmp(self.config)

		self.widgets=[]

		self.setup_devices()

	def setup_devices(self):
		for widget in self.widgets:
			widget.destroy()

		self.widgets=[]

		self.devices=self.load_devices()

		for device in self.devices.values():
			if 'dimmer' in device['model']:
				widget=Dimmer(self, title=device['name'])
				widget.callback(self.dim, [ device['index'] ])
			else:
				widget=Switch(self, title=device['name'])
				widget.callback(self.toggle, [ device['index'] ])

			widget.set(device['value'])

			widget.pack()

			self.widgets.append(widget)

	def load_devices(self):
		data=self.snmp.walk(self.mibroot)

		rmib={v:k for k,v in self.mib.items()}

		devices={}

		for row in data:
			if not row.oid_index in devices:
				devices[row.oid_index]={}

			devices[row.oid_index][rmib[row.oid]]=row.value

		return devices

	def toggle(self, index):
		print("XXX Not implemented, I don't have a non-dimming switch")

	def dim(self, level, index):
		self.snmp.set("{}.{}".format(self.mib['value'], index), level, 'GAUGE')

class Device(Frame):
	def __init__(self, parent):
		super().__init__(parent)

	def set(self, value):
		self.value=value

	def get(self):
		return self.value

	def callback(self, callback, params=[]):
		self.callback=callback
		self.params=params

class Dimmer(Device):
	def __init__(self, parent, title="Dimmer"):
		super().__init__(parent)

		self.label=Label(self, text=title)
		self.label.pack()
		self.scale=Scale(self, from_=0, to=255, orient=HORIZONTAL)
		self.scale.pack()
		self.button=Button(self, text="Set", command=self.press)
		self.button.pack()

	def set(self, value):
		super().set(value)
		self.scale.set(value)

	def press(self):
		if self.callback:
			self.callback(self.scale.get(), *self.params)

class Switch(Device):
	def __init__(self, parent, title="Switch"):
		super().__init__(parent)

		self.label=Label(self, text=title)
		self.label.pack()
		self.button=Button(self, text="Toggle", command=self.press)
		self.button.pack()

	def press(self):
		if self.callback:
			self.callback(*self.params)
