import binascii
import random
import string
import operator
import struct

def hash(key):
	result = 0
	prev_result = 0
	for i in range(len(key)):
		current_char = ord(key[i])
		result = operator.imul(prev_result, 0x24)
		result += prev_result
		result += current_char
		prev_result = result
		prev_result = prev_result & 0xffffffff #keep it in 32bit range

	return prev_result

ascii_chars = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789+/!$%^&*()-_={}[]~#@?|<>.,"
keys = [0xee613e2f, 0xde79eb45, 0xaf1b2f3d, 0x8747bbd7, 0x739ac49c, 0xc9a4f5ae, 0x4632c5c1, 0xa0029b24, 0xd6165059, 0xa6b79451, 0xe79d23ba, 0x8aae92ce, 0x85991a18, 0xfee05899, 0x430c7994, 0x1ab9f36f, 0x70c42481, 0x05bd27cf, 0xc4ff6e6f, 0x5a77847c, 0xdd9277b3, 0x25843cff, 0x5fdca944, 0x8ee42896, 0x2ae961c7, 0xa77731da]

current_key = [' ', ' ', 'F', 'L', 'A', 'R', 'E', ' ', 'O', 'n', '!']

c2 = 0x5f
final = []

k_index = 0
while k_index < len(keys):
	c1 = random.choice(ascii_chars)
	c2 += 1
	current_key[0] = c1
	current_key[1] = chr(c2)
	required = keys[k_index]

	print "[+] Attacking %d" %required
	
	while True:
		result = hash(''.join(current_key))

		if result == required:
			print "[+] Found key for %d: %s" %(required, ''.join(current_key))
			final.append(current_key[0])
			break
		else:	
			current_key[0] = random.choice(ascii_chars)

	k_index += 1

print ''.join(final)
