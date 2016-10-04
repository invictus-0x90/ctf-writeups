import os

#simple zip cracker, nothing special, but using the system command works better than using the python zip functions (they dont work)
def main():
	fp = open("/usr/share/wordlists/rockyou.txt")
	ret_code = 512
	
	for line in fp.readlines():
		#the \' \' characters deal with a problem with passwords that have a space in them
		command = "7z t acmeenergy_systemarchitecture.zip -p\'" + line.strip('\n') + "\'"
		s = os.system(command)
		if s == 0:
			print "[+] Found Passwd [+]"
			print line
			break

if __name__ == '__main__':
	main()
