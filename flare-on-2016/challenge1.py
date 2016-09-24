import hashlib
import socket
import base64
import binascii
import random
import string

my_str = "paa"
req = "x2dtJEOmyjacxDemx2eczT5cVS9fVUGvWTuZWjuexjRqy24rV29q"
	   #sh00ti     phi             arr     fla         com
print "length should be: 39"
alphabet = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789+/"
ascii_chars = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789+/!$%^&*()-_={}[]~#@?|<>.,"
		  # 0123456789012345678901234567890123456789012345678901234567890123


def crypt(length, my_str):
	index = 0
	result = []
	alpha_len = len(alphabet)

	while index < length:
		if index >= length:
			break
		c1 = ord(my_str[index])
		index += 1
		if index >= length:
			break
		c2 = ord(my_str[index])
		index += 1
		if index >= length:
			break
		c3 = ord(my_str[index])
		index += 1

		c1 = c1 << 16 #shl edx, 10
		c2 = c2 << 8 #shl eax, 8
		c1 = c1 + c3 #ie 00410000 + 00000041
		c2 = c1 + c2 #ie 00410041 + 00004100

		current = c2
		current = current >> 18
		result.append(alphabet[current % alpha_len])

		current = c2 #reload result from previous calcs
		current = current >> 12
		result.append(alphabet[current % alpha_len])

		current = c2
		current = current >> 6
		result.append(alphabet[current % alpha_len])
	
		current = c2
		current = current >> 0
		result.append(alphabet[current % alpha_len])
	return result


def randomword(length):
   return ''.join(random.choice(ascii_chars) for i in range(length))


counter = 0
wins = 0
final = ""
while(True):
	attempt = randomword(3)
	result = "".join(crypt(len(attempt), attempt))
	attacking = req[wins:wins+4]
	print "attacking: %s" %attacking

	if(result == attacking):
		print "[+] found a new value for %s[+]" %attacking
		print attempt
		final += attempt
		wins += 4
	if wins >= len(req):
		break
	if counter == 3000000:
		print "[!] Taking ages on: %s" %attacking
		counter = 0
	counter += 1

print final