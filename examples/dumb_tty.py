import sys, argparse, pyhypnolsd
import Adafruit_BBIO.UART as UART

def dumb_tty(port):
	"""
	Simple dumb TTY that allows you to execute commands in Command
	Mode. Bit buggy when reading output. Good demo of CommandMode

	Parameters
	----------
	port : string
		the dir to the TTY or COM port

	"""
	UART.setup("UART1")
	hlsd = pyhypnolsd.command_mode.CommandMode(port)

	get_command = True
	while (get_command):
		# Get input
		command = raw_input("> ")

		# Check for exit
		if (command == "exit"):
			get_command = False
			continue

		# Send command
		hlsd.send_command(command)

		# Read output
		hlsd.read_response()

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