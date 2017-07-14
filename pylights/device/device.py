# vim:ts=4:sw=4:

from tkinter import *

class Device(Frame):
	def __init__(self, parent):
		super().__init__(parent)

	def set(self, value):
		self.value=value

	def get(self):
		return self.value

	def setSetCallback(self, callback, params=[]):
		self.setcallback=callback
		self.setparams=params

	def setGetCallback(self, callback, params=[]):
		self.getcallback=callback
		self.getparams=params
