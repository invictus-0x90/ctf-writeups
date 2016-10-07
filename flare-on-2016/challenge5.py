#!/usr/bin/env python

counter = 0
index = 9
word_40df1a = 0
word_40df18 = 0
memory = 0
ss = "kYwxCbJoLp"
my_buffer = \
	[item for sublist in [[ord(c),0] for c in ss] \
		for item in sublist] \
	+ [0]*0xff

f = open("C:\\Users\\name\\Desktop\\flare_on\\challenge5\\smokesta_0040A000.mem", "rb")

memory = []

#load the memory dumped from ollydbg into our own buffer
for b in f.read():
	memory.append(b)

def get_memory(arg):
	return (ord(memory[arg*2+1])<<8) + ord(memory[arg*2])

def sub_401000(arg_1):
	global index, my_buffer
	index += 1
	my_buffer[index*2] = arg_1 & 0xff
	my_buffer[index*2+1] = (arg_1 >> 8) & 0xff
	
def sub_401030():
	global counter, memory
	counter += 1
	var_1 = get_memory(counter)
	sub_401000(var_1)
	counter += 1

def sub_401080():
	global index, my_buffer
	ret = (my_buffer[index*2+1]<<8) + my_buffer[index*2]
	#var_1 = my_buffer[index]
	index -= 1
	print "returning index : %d" %ret
	return ret

def sub_4010c0():
	global counter
	counter += 1
	sub_401080()
	
def sub_4010e0():
	global counter
	var_1 = sub_401080()
	var_2 = sub_401080()
	var_3 = var_2 + var_1
	sub_401000(var_3)
	counter += 1

def sub_401130():
	global counter
	var_1 = sub_401080()
	var_2 = sub_401080()
	var_3 = var_2 - var_1
	sub_401000(var_3)
	counter += 1

def sub_401180():
	global counter
	var_1 = sub_401080()
	var_2 = sub_401080()
	
	sub_401000((var_2 << (0x10-var_1)) | (var_2 >> var_1))
	counter += 1

def sub_4011f0():
	global counter
	var_1 = sub_401080()
	var_2 = sub_401080()
	
	sub_401000((var_2 >> (0x10-var_1)) | (var_2 << var_1))
	counter += 1

def sub_401260():
	global counter
	var_1 = sub_401080()
	var_2 = sub_401080()
	var_3 = var_2 ^ var_1
	sub_401000(var_3)
	counter += 1

def sub_4012b0():
	global counter
	var_1 = sub_401080()
	var_2 = (~var_1) 
	sub_401000(var_2)
	counter += 1
	

def sub_401300():
	global counter
	var_1 = sub_401080()
	var_2 = sub_401080()
	if var_1 == var_2:
		var_3 = 1
	else:
		var_3 = 0
	sub_401000(var_3)
	counter += 1
	
def sub_401360():
	global counter
	var_2 = sub_401080()
	var_3 = sub_401080()
	var_1 = sub_401080()
	if(var_1 == 1):
		sub_401000(var_2)
	else:
		sub_401000(var_3)
	counter += 1

def sub_4013c0():
	global counter
	counter = sub_401080()

#NOT COMPLETE
def sub_4013d0():
	global counter, word_40df1a, index, word_40df18
	counter += 1
	var_2 = get_memory(counter)
	var_3 = var_2
	var_1 = 0
	if(var_3 == 0):
		var_1 = word_40df18
	elif(var_3 == 1):
		var_1 = word_40df1a
	elif(var_3 == 2):
		var_1 = index
	elif(var_3 == 3):
		var_1 = counter
	sub_401000(var_1)
	counter += 1

def sub_401480():
	global counter, word_40df18, word_40df1a, index
	counter += 1
	var_2 = get_memory(counter)
	var_1 = sub_401080()
	var_3 = var_2
	if(var_3 == 0):
		word_40df18 = var_1
	elif(var_3 == 1):
		word_40df1a = var_1
	elif(var_3 == 2):
		index = var_1
	elif(var_3 == 3):
		counter = var_1
	counter += 1

def sub_401520():
	global counter
	counter += 1

def sub_401540():
	global func_buffer, memory, counter, index
	var_1 = get_memory(counter)
	#print "var_1 = %d" %var_1
	func = func_buffer[var_1]
	func()
	
#sub_401610
def main():
	global counter, index, my_buffer
	s = ''
	while counter < 0x182:
		print "counter = %d" %(counter)
		print "index = %d" %index

		sub_401540()
	for c in my_buffer:
		if c != 0:
			s += ''.join(chr(c))
	print s
	
func_buffer = [sub_401030, sub_4010c0, sub_4010e0, sub_401130, sub_401180, sub_4011f0, sub_401260, sub_4012b0, sub_401300, sub_401360, sub_4013c0, sub_4013d0, sub_401480, sub_401520]

main()
