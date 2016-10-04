// challenge4.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>
#include <WinUser.h>


typedef void(__cdecl *beep)(int, int);
int main()
{
	HMODULE dll;
	FARPROC fn;
	LPCSTR name;

	dll = LoadLibrary(L"C:\\flareon2016challenge.dll");
	

	if (dll == NULL)
	{
		printf("[!] Could not load DLL for challenge [!]\n");
	}
	else
	{
		/* The order is incredibly important, need to figure this out properly */
		int order[] = { 40,32,35,11,17,10,47,7,46,38,22,19,3,23,8,16,20,5,6,48,15,9,42,25,1,41,36,26,43,45,29,34,39,13,21,12,44,33,37,27,14,18,4,2,30,31,28,24,51,49,50 };
		int size = sizeof(order) / sizeof(int);
		for (int i = 0; i < size; i++)
		{
			name = MAKEINTRESOURCEA(order[i]);
			fn = GetProcAddress(dll, name);

			if (i == 50)
			{
				for (int i = 0; i < 18; i++)
				{
					beep func = (beep)fn;
					//func(freq, dur) the args to this function change the encrypted string that is returned
					func(1337, 1337); //random arg
				}
			}
			else
			{
				fn();
			}
		}
		
	}
    return 0;
}

