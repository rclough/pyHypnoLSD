""" 
Module that contains various functions, constants, and tools
for interacting with a hypnoLSD object
"""
import sys, serial


###############################################################################
# Constants
###############################################################################

NATIVE_BAUD = 9600
MAX_BAUD = 12000000
COMMAND_MODE = 0
DRAW_MODE = 1
READLINE_TIMEOUT = 0.5
SYNC_BYTE = b'0xFE'

###############################################################################
# Utility methods
###############################################################################

def baud_from_divisor(divisor):
	""" 
	Returns the baud rate, given a divisor.

	Parameters
	----------
	divisor : int
		baud rate divisor for the HypnoLSD. See HypnoLSD
		docs for more details

	"""
	return MAX_BAUD / (int(divisor)+1)

def divisor_from_baud(baud) :
	""" 
	Returns the divisor, given a baud rate. ints only please 

	Parameters
	----------
	baud : int
		baud rate you'd like to operate at, and need the divisor
		for to set speed on the HypnoLSD

	"""
	return int(MAX_BAUD/int(baud))-1

###############################################################################
# HypnoLSD class
###############################################################################

class HypnoLSD:
	"""
	Class meant to symbolize a single HypnoLSD module. Tracks the state
	of the module so that it may be used by different convenience interfaces, 
	or used directly.

	By default, demo is turned off because it is useless when programming.

	"""
	def __init__(self, port, baudrate=NATIVE_BAUD):
		# Initialize internal variables
		self.mode = COMMAND_MODE

		# Initialize serial connection
		self.serial = serial.Serial(port=port, baudrate=NATIVE_BAUD, timeout=READLINE_TIMEOUT)
		self.serial.close()
		self.serial.open()

		# Turn off demo mode
		self.demo_off()

		# Update baud rate if necessary
		if baudrate != NATIVE_BAUD:
			self.change_baudrate(baudrate)

	def change_baudrate(self, baudrate):
		""" Change the baud rate used to speak to HypnoLSD """
		if baudrate == self.serial.baudrate:
			return ["Baudrate already set to " + str(baudrate)]

		divisor = divisor_from_baud(baudrate)
		return self.change_divisor(divisor, baudrate)

	def change_divisor(self, divisor, baudrate=False):
		""" Change the baud rate divisor on the HypnoLSD """
		if not baudrate:
			baudrate = baud_from_divisor(divisor)
			if baudrate == self.serial.baudrate:
				return ["Baudrate already set to " + str(baudrate)]

		# Send command
		response = self.send_command("set speed " + str(divisor))
		self.serial.flush() # Flush command so we can read output with new baud rate
		self.serial.baudrate = baudrate
		return response

	def send_command(self, command, override=False, print_it=False):
		""" 
		Send a command to HypnoLSD, only available in Command Mode

		Parameters
		----------
		command : string
			Command to send to HypnoLSD, with no return chars
		override : boolean (optional)
			Set true if you want to switch modes (if currently in draw mode) 
			so you can send the command.
		resp : boolean (optional)
			Set true if you want to return the response (list of strings)

		"""

		# Check modes
		if self.mode == DRAW_MODE and not override:
			print "Currently in Draw Mode, cannot execute commands"
			return
		elif self.mode == DRAW_MODE and override:
			self.draw_mode()

		# Execute command
		self.serial.write(command+"\r\n")

		return self.get_response(print_it)

	def get_response(self, print_it=False, break_on_OK=True):
		""" 
		Get one HypnoLSD response, a list of lines.

		Parameters
		----------
		print_it : boolean (optional)
			Print the output to stdout
		break_on_OK : boolean (optional)
			If set true, it will only print up to the last "OK".
			This can speed up program flow if you are retrieving responses
			for each command you send.  When set to false, it will spit out
			everything available for it to spit out.

		"""
		response = []
		has_serial = True
		while has_serial:
			# Keep reading lines from serial until you timeout
			from_serial = self.serial.readline()
			if not from_serial:
				has_serial = False
			else:
				response.append(from_serial.strip())
				if print_it:
					sys.stdout.write(from_serial)
				if break_on_OK and from_serial == "OK\r\n":
					break

		if print_it:
			sys.stdout.flush()
		return response

	def command_mode(self):
		""" Put HypnoLSD in Command Mode """
		self.serial.write(SYNC_BYTE+SYNC_BYTE)
		self.mode = COMMAND_MODE

	def draw_mode(self):
		""" Put HypnoLSD in Draw Mode """
		if self.mode == DRAW_MODE:
			return

		self.send_command("draw")
		self.mode = DRAW_MODE

	def demo_off(self):
		""" Turn off demo mode. Useless when coding. """
		self.send_command("demodelay 0")
		self.get_response(break_on_OK=False) # swallow response

	def close(self):
		""" Close connection to HypnoLSD """
		self.change_baudrate(NATIVE_BAUD)
		self.serial.close()

	def flush(self):
		""" Flush inputs and outputs of device """
		self.serial.flush()





