import Adafruit_BBIO.UART as UART
import serial
import sys
import time
import re

MAX_BAUD = 12000000
baud = 9600
new_baud = False

speed_change = re.compile("set speed [0-9]*")

# Basic setup for BBB serial communication
UART.setup("UART1")
ser = serial.Serial(port = "/dev/ttyO1", baudrate=baud, timeout=0.3)
ser.close()
ser.open()

ready = True
while (ready):
	# Get input
	command = raw_input("> ")

	# Check for exit
	if (command == "exit"):
		ready = False
		continue

	# Check for "set speed"
	if speed_change.match(command):
		divisor = int(command.split("set speed ")[1])
		baud = int(MAX_BAUD/(divisor+1))
		new_baud = True
		print("Divisor change to " + str(divisor) + 
			", baud to be set to " + str(baud))

	# Send command
	has_serial = True
	ser.write(command+"\r\n")

	# Set new baudrate if needed
	if (new_baud):
		new_baud = False
		ser.flush() # wait for baud change to send
		ser.baudrate = baud

	# Read return
	while has_serial:
		from_serial = ser.readline()
		if not from_serial:
			has_serial = False
		else:
			sys.stdout.write(from_serial)
	sys.stdout.flush()
	print("")

ser.close()