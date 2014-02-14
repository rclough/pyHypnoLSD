#!/usr/bin/env python
import sys, argparse, pyhypnolsd
import Adafruit_BBIO.UART as UART

def dumb_tty(port):
	"""
	Simple dumb TTY that allows you to execute commands in Command
	Mode. Bit buggy when reading output. Good demo of CommandMode.

	Dependency on Adafruit_BBIO, but may be removed if your UART is
	already prepared.

	Parameters
	----------
	port : string
		the dir to the TTY or COM port

	"""
	UART.setup("UART1")
	hlsd = pyhypnolsd.command_mode.from_port(port)

	get_command = True
	while (get_command):
		# Get input
		command = raw_input("> ")

		# Check for exit
		if (command == "exit"):
			get_command = False
			continue

		# Send command, let it print output
		hlsd.send_command(command, True)

	# Close remaining connections
	hlsd.close()


def process_arguments():
	'''Argparse function to get the program parameters'''

	parser = argparse.ArgumentParser(description='Dumb TTY for interacting with HypnoLSD module')

	parser.add_argument(    'port',
                            action      =   'store',
                            help        =   'path to the TTY (or com port in windows)')

	return vars(parser.parse_args(sys.argv[1:]))

if __name__ == '__main__':
    # get the parameters
    parameters = process_arguments()

    # Run the dumb tty
    dumb_tty(parameters['port'])