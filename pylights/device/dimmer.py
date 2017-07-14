# vim:ts=4:sw=4:

from tkinter import *
from .device import Device

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

	def get(self):
		if self.getcallback:
			self.set(self.getcallback(*self.getparams))

		return super().get()

	def press(self, event):
		if self.setcallback:
			self.setcallback(self.scale.get(), *self.setparams)
