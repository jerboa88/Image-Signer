from sys import argv, exit
import numpy as np
from skimage import io, data
from statistics import mode, StatisticsError
from timeit import default_timer as timer
from itertools import groupby


sensitivity = 80
upper = 255 - sensitivity
separator_code = ['0', '0', '1', '1', '1', '0', '1']
verbose = True
opacity = 1
start_time = timer()


vprint = print if verbose else lambda *a, **k: None



# Prints an error message and exits the program
def progress(*strings):
	print(*strings, '%)', sep='', end='\r', flush=True)



def printtime():
	print('\nFINISHED IN', round(timer() - start_time, 2), 'seconds')



# Prints an error message and exits the program
def error(*strings):
	print('ERROR:', *strings)
	exit(1)



def loadimage(filename):
	try:
		return io.imread(filename)

	except:
		error('The image could not be found')



# Takes a pixel as input and returns True is the pixel is white and False if it is not
def iswhite(pixel):
	return True if pixel[0] > upper and pixel[1] > upper and pixel[2] > upper else False



# Takes an image array, and starting x and y coordinates as input and searches for messages in the image. Returns a single decoded string
def decodeline(row, starting_x, width):
	bit_array = []
	message_array = []
	undefined_bit_array = ['1'] * 7

	if starting_x < width:
		for i in range(starting_x, width - 7, 7):
			char_bit_array = ['0'] * 7

			for j in range(3):
				# char_bit_array[j] = '1' if iswhite(row[i+j])
				if iswhite(row[i+j]):
					char_bit_array[j] = '1'

			if char_bit_array[0] == '0' and char_bit_array[1] == '0':
				if char_bit_array[2] == '0':
					bit_array.extend(undefined_bit_array)

				else:
					for j in range(3, 7):
						# char_bit_array[j] = '1' if iswhite(row[i+j])
						if iswhite(row[i+j]):
							char_bit_array[j] = '1'

					if char_bit_array[3] == '1' and char_bit_array[4] == '1' and char_bit_array[5] == '0' and char_bit_array[6] == '1':
						i += 7
						message_array.append(bit_array)
						bit_array = []

					else:
						bit_array.extend(undefined_bit_array)

			else:
				for j in range(3, 7):
					# char_bit_array[j] = '1' if iswhite(row[i+j])
					if iswhite(row[i+j]):
						char_bit_array[j] = '1'

				bit_array.extend(char_bit_array)

		message_array.append(bit_array)

	for k in range(len(message_array)):
		bit_string = ''.join(message_array[k])

		output_string = ''

		for i in range(0, len(bit_string), 7):
			char = '0b'

			for j in range(7):
				char += bit_string[i + j]

			char_value = chr(int(char, 2))

			if char_value == '\x7f':
				char_value = '\xbf'

			output_string += char_value

		message_array[k] = output_string.rstrip('\xbf ')

	return message_array



def findseparator(filename):
	img = loadimage(filename)
	height = len(img)
	width = len(img[0])
	width_padded = width - 7
	leading_separators = []
	messages = []

	for y in range(height):
		row = img[y]

		for x in range(0, width_padded, 7):
			if not iswhite(row[x]) and not iswhite(row[x+1]) and iswhite(row[x+2]) and iswhite(row[x+3]) and iswhite(row[x+4]) and not iswhite(row[x+5]) and iswhite(row[x+6]):
				leading_separators.append((y, x))
				progress('FOUND SEPARATOR AT ', y, ' ', x, ' (', (y + 1) * 100 // height)
				break	# Stop after leading separator is found

	print()


	leading_separators_length = len(leading_separators)

	for i in range(leading_separators_length):
		message_start = leading_separators[i][1] + 7
		progress('DECODING MESSAGE STARTING AT ', leading_separators[i][0], ' ', message_start, ' (', (i + 1) * 100 // leading_separators_length)

		decoded_string_array = decodeline(img[leading_separators[i][0]], message_start, width)

		for decoded_string in decoded_string_array:
			if decoded_string:
				messages.append([decoded_string, 0])


	char_counts = {}

	if messages:
		for i in range(len(messages[0][0])):
			char_counts[i] = []

			for j in range(len(messages)):
				if i < len(messages[j][0]):
					current_char = messages[j][0][i]

					if current_char != '\xbf':
						char_counts[i].append(current_char)

					else:
						messages[j][1] += 1

	else:
		error('No messages were found')

	messages.sort(key = lambda x: (-len(x[0]), x[1]))	# Sort first by length and then by # of unknown characters

	messages = list(messages for messages, _ in groupby(messages))

	print('\nEXTRACTED MESSAGES:')
	for i in range(len(messages)):
		if messages[i]:
			print(messages[i][0])

	print()

	computed_string = []

	for key in char_counts:
		try:
			if char_counts[key]:
				most_common_char = mode(char_counts[key])

			else:
				most_common_char = '\xbf'


		except StatisticsError:
			most_common_char = char_counts[key][0]

		computed_string.append(most_common_char)

	print('COMPUTED MESSAGE:', ''.join(computed_string))
	printtime()



def ceil(value):
	return 255 if value > 255 else value



def floor(value):
	return 0 if value < 0 else value



# Writes a single line to an image given a starting coordinate
def writeline(row, segment_bit_array, segment_length, min_width, width, tint):
	if min_width <= width:
		for i in range(7):
			pixel = row[i]
			row[i] = [ceil(pixel[0] + tint), ceil(pixel[1] + tint), ceil(pixel[2] + tint)] if separator_code[i] == '1' else [floor(pixel[0] - tint), floor(pixel[1] - tint), floor(pixel[2] - tint)]


		for x in range(7, width):
			pixel = row[x]
			row[x] = [ceil(pixel[0] + tint), ceil(pixel[1] + tint), ceil(pixel[2] + tint)] if segment_bit_array[(x - 7) % segment_length] == '1' else [floor(pixel[0] - tint), floor(pixel[1] - tint), floor(pixel[2] - tint)]

	else:
		error('Image is not wide enough. The image needs to be at least', min_width, 'pixels wide. Please choose a shorter string')



# Encodes an array of bits into an image. Takes an input filename, an output filename, and an array of bits as input
def signimg(filename, output_filename, bit_array, ratio):
	img = loadimage(filename)
	height = len(img)
	width = len(img[0])
	bit_array_length = len(bit_array)

	segment_length = bit_array_length + 7
	min_width = segment_length + 7
	bit_array.extend(separator_code)
	tint = 255 * opacity
	# a = np.array(bit_array)
	# a[a == '1'] = 2555
	# print(a)

	if ratio == 0:
		writeline(img[0], bit_array, segment_length, min_width, width, tint) # Do it once only

	else:
		if ratio < 0:
			ratio = height

		increment = height // ratio	# How many pixels between lines

		for i in range(0, height, increment):
			value = (i + 1) // increment

			progress('WRITING LINE ', value, '/', ratio, ' (', value * 100 // ratio)
			writeline(img[i], bit_array, segment_length, min_width, width, tint)

	io.imsave(output_filename, img, check_contrast=False, quality=100)
	printtime()



# Takes a string as input, encodes it, and returns an array of bits
def encode(input_string):
	bit_array = []

	print('\nENCODING:', input_string)

	for i in range(len(input_string)):
		encoded_char = bin(ord(input_string[i][0]))[2:].zfill(7)

		for j in range(len(encoded_char)):
			bit_array.append(encoded_char[j])

	return bit_array



def main():
	args = len(argv)

	if args > 3:
		if argv[1] == 'sign':
			complete_filename = argv[2].split('.')

			if complete_filename:
				output_file_name = complete_filename[0] + '_signed.' + complete_filename[1]

				if args == 5:
					try:
						ratio = int(argv[4])

					except:
						error('The ratio you entered is not a number')

				else:
					ratio = 0

				print('* STARTING SIGN OF STRING \'' + argv[3] + '\' INTO', output_file_name, '*')
				signimg(argv[2], output_file_name, encode(argv[3]), ratio)

			else:
				error('Invalid filename provided')

		elif argv[1] == 'read':
			error('Invalid arguments provided. Please enter \'sign\' followed by the file name, and a message.')

		else:
			error('Invalid arguments provided. Please enter \'sign\' or \'read\'.')

	elif args == 3:
		if argv[1] == 'read':
			print('* STARTING READ OF', argv[2], '*')
			findseparator(argv[2])

		elif argv[1] == 'sign':
			error('Invalid arguments provided. Please enter \'read\' followed by the file name.')

		else:
			error('Invalid arguments provided. Please enter \'sign\' or \'read\'.')

	elif args == 2:
		error('No filename provided')

	elif args == 1:
		error('No arguments were given')

	else:
		error('Too many arguments were given')



main()
