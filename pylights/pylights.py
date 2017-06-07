# vim:ts=4:sw=4:

from tkinter import *
from collections import OrderedDict

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
		self.config=config
		self.snmp=Snmp(self.config)
		self.widgets=[]

		root=Tk()
		root.title('PyLights')
		root.resizable(0,0)

		super().__init__(root)
		self.pack()

		self.menu=Menu(self)
		filemenu=Menu(self.menu, tearoff=0)
		filemenu.add_command(label="Rescan devices", command=self.setup_devices)
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
				widget.callback(self.dim, [ device['index'] ])
			else:
				widget=Switch(self, title=device['name'])
				widget.callback(self.set, [ device['index'] ])

			widget.set(device['value'])

			widget.pack()

			self.widgets.append(widget)

	def load_devices(self):
		data=self.snmp.walk(self.mibroot)

		rmib=OrderedDict({v:k for k,v in self.mib.items()})

		devices={}

		for row in data:
			if not row.oid_index in devices:
				devices[row.oid_index]={}

			devices[row.oid_index][rmib[row.oid]]=row.value

		return devices

	def set(self, state, index):
		self.snmp.set("{}.{}".format(self.mib['value'], index), state, 'GAUGE')

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
		self.scale.bind('<ButtonRelease-1>', self.press)
		self.scale.pack()

	def set(self, value):
		super().set(value)
		self.scale.set(value)

	def press(self, event):
		if self.callback:
			self.callback(self.scale.get(), *self.params)

class Switch(Device):
	def __init__(self, parent, title="Switch"):
		super().__init__(parent)

		self.label=Label(self, text=title)
		self.label.pack()
		self.on=Button(self, text="On", command=self.on)
		self.on.pack(side=LEFT)
		self.off=Button(self, text="Off", command=self.off)
		self.off.pack(side=RIGHT)

	def on(self):
		if self.callback:
			self.callback(1, *self.params)

	def off(self):
		if self.callback:
			self.callback(0, *self.params)
