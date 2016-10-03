// challenge4.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <Windows.h>
#include <WinUser.h>


typedef void(__cdecl *uef)(int, int);
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
				/* call func.50 with args 
				*  this function takes two args, freq and duration (cdecl format).
				*  the function then builds a "key" that is used to decrypt(?) data once it has been called 18 times.
				*/
				if (i == 50)
				{
					/* Think this function needs to be run 18 times */
					for (int i = 0; i < 18; i++)
					{
						uef func = (uef)fn;
						func(300, 600); //random arg
					}
					
				}
				/* else no args */
				else
				{
					fn();
				}
			}
		}

	}



    return 0;
}

