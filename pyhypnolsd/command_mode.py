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

	def __init__(self,port):
		"""
		Initialize CommandMode Object 

		Parameters
		----------
		port : string
			Serial port directory, ex: /dev/tty01

		"""
		self.new_baud = False
		self.baud = hypnolsd.NATIVE_BAUD
		self.serial = serial.Serial(port=port, baudrate=self.baud, timeout=0.3)
		self.serial.close()
		self.serial.open()

	def send_command(self,command):
		"""
		Send a command to the HypnoLSD

		Parameters
		----------
		command : string
			A command string with no return characters

		"""
		# Special case: if user tries to adjust speed, we need to 
		# change the baud rate with it
		if SET_SPEED_REGEX.match(command):
			divisor = int(command.split("set speed ")[1])
			self.baud = hypnolsd.baud_from_divisor(divisor)
			self.new_baud = True
			print("Divisor change to " + str(divisor) + 
				", baud to be set to " + str(self.baud))

		self.serial.write(command+"\r\n")

	def read_response(self):
		""" 
		Should be called immediately after making a command, if you care about
		the output. Output format not guaranteed during command mode due to
		output from the default demo programs

		"""

		# Change baud rate if we haven't read since last change
		if (self.new_baud):
			self.new_baud = False
			self.serial.flush() # wait for baud change to send
			self.serial.baudrate = self.baud

		# Read
		has_serial = True
		while has_serial:
			from_serial = self.serial.readline()
			if not from_serial:
				has_serial = False
			else:
				sys.stdout.write(from_serial)
				if from_serial == "OK\r\n":
					break
		sys.stdout.flush()

	def close(self):
		""" Close connection to HypnoLSD """
		self.serial.close()
