// challenge4.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>
#include <WinUser.h>


typedef void(__cdecl *beep)(int, int); //specifies that we must clear the stack on return
int main()
{
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
		/* The order is incredibly important, need to figure this out properly */
		/* Possible order, gained from the return value from each function stored in eax */
		int order[] = {0,35,22,25,9,45,23,36,2,12,37,14,18,8,46,30,7,4,42,34,47,11,32,27,39,10,3,21,13,16,33,26,17,44,6,20,48,19,29,38,24,15,41,31,28,43,5,40};
		int size = sizeof(order) / sizeof(int);
		for (int i = 0; i < size; i++)
		{
			name = MAKEINTRESOURCEA(order[i]);
			fn = GetProcAddress(dll, name);
			if(fn != NULL)
			{
				fn();
			}
		}
		/* Call function 51 */
		name = MAKEINTRESOURCEA(51);
		fn = GetProcAddress(dll, name);
		fn();
		
		/* Get address of function 50 (beep function) */
		name = MAKEINTRESOURCEA(50);
		fn = GetProcAddress(dll, name);
		func = (beep)fn;

		int freq = 300, dur = 59;
		for (int i = 0; i < 18; i++)
		{
			//func(freq, dur) the args to this function change the encrypted string that is returned
			func(freq, dur); //random arg
		}

		
	}
    return 0;
}

