// challenge4.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>
#include <WinUser.h>



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
		/* At the moment all i can think to do is call each function sequentially */
		for (int i = 0; i < 52; i++)
		{
			name = MAKEINTRESOURCEA(i); //MAKEINTRESOURCEA returns an LPCSTR we can use as an ordinal value
			fn = GetProcAddress(dll, name);
			if (fn != NULL)
			{
				/* Obviously Im not passing any arguments here, need to fix that */
				fn();
			}
		}

	}



    return 0;
}

