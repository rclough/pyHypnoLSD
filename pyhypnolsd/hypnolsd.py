""" Constants and utility methods relevant to the HypnoLSD module """
NATIVE_BAUD = 9600
MAX_BAUD = 12000000

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