# vim:ts=4:sw=4:

from tkinter import *
from .device import Device

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
		if self.setcallback:
			self.setcallback(1, *self.setparams)

	def off(self):
		if self.setcallback:
			self.setcallback(0, *self.setparams)
