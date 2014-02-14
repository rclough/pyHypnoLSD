#!/usr/bin/env python
"""Tools for 'Command Mode' interfacing"""
import sys, re, serial, hypnolsd

SET_SPEED_REGEX = re.compile("set speed [0-9]*")

class CommandMode():
	"""
	CommandMode class

	Represents a single object which can be instantiated to interact
	with the HypnoLSD module in 'Command Mode'. Please do not try
	and connect more than one, as the serial port will be busy!

	Also do close() the connection!

	Currently only supports initialized 9600 baud rate, as command mode 
	doesn't really need speed. Can be adjusted once started.
	"""

	def __init__(self,hypnolsd):
		"""
		Initialize CommandMode Object 

		Parameters
		----------
		port : string
			Serial port directory, ex: /dev/tty01

		"""
		self.hypnolsd = hypnolsd
		self.new_baud = False

	def send_command(self,command, print_it=False):
		"""
		Send a command to the HypnoLSD. Overrides "set speed nnnn" to
		handle complexities of baudrate changes

		Parameters
		----------
		command : string
			A command string with no return characters
		print_it : boolean (optional)
			True if you want to actively print the response as its received

		Returns
		-------
		response : list
			List of strings of the response

		"""
		# Special case: if user tries to adjust speed, use actual method
		if SET_SPEED_REGEX.match(command):
			divisor = int(command.split("set speed ")[1])
			return self.hypnolsd.change_divisor(divisor)

		# Special case: Draw mode not supported
		if command == "draw":
			print("Draw Mode not supported from CommandMode object")
			return ["Draw Mode not supported from CommandMode object"]

		return self.hypnolsd.send_command(command, print_it=print_it)

	def close(self):
		""" Close connection to HypnoLSD """
		self.hypnolsd.close()

def from_port(port):
	"""
	Convenience method to generate a CommandMode object given only the port.
	Creates a HypnoLSD object first and then instantiates the CommandMode object
	with it.

	"""
	return CommandMode(hypnolsd.HypnoLSD(port))
