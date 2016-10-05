// challenge4.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>
#include <WinUser.h>

//571F8460  4E E6 40 BB B1 19 BF 44  Næ@»±¿D


typedef void(__cdecl *beep)(int, int); //specifies that we must clear the stack on return
int main()
{
	unsigned int k1 = 0xbb40e64e, k2 = 0x44bf19b1;
	HMODULE dll;
	FARPROC fn;
	LPCSTR name;
	beep func;

	dll = LoadLibrary(L"C:\\flareon2016challenge.dll"); //load the library

	if (dll == NULL)
	{
		printf("[!] Could not load DLL for challenge [!]\n");
	}
	else
	{
		int next = 30; //start with function 30
		for (int i = 0; i < 49; i++)
		{
			name = MAKEINTRESOURCEA(next);
			fn = GetProcAddress(dll, name);
			if (fn != NULL)
			{
				next = fn();
			}
		}

		/* The order is incredibly important, need to figure this out properly */
		/* Possible order, gained from the return value from each function stored in eax */
		int order[] = { 35,22,25,9,45,23,36,2,12,37,14,18,8,46,30,7,4,42,34,47,11,32,27,39,10,3,21,13,16,33,26,17,44,6,20,48,19,29,38,24,15,41,31,28,43,5,40,1 };

		/* Get address of function 50 (beep function) */
		name = MAKEINTRESOURCEA(50);
		fn = GetProcAddress(dll, name);
		func = (beep)fn;
		int freq[] = {0x1b8, 0x1b8, 0x1b8, 0x15d, 0x20b, 0x1b8, 0x15d, 0x20b, 0x1b8, 0x293, 0x293, 0x293, 0x2ba, 0x20b, 0x19f, 0x15d, 0x20b, 0x1b8};
		int dur[] = { 500, 500, 500, 350, 150, 500, 350, 150, 1000, 500, 500, 500, 350, 150, 500, 350, 150, 1000 };
		//int freq = 300, dur = 59;
		for (int i = 0; i < 18; i++)
		{
			func(freq[i], dur[i]);
		}
	}
	return 0;
}

