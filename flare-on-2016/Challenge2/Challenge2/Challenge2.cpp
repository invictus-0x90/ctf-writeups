// challenge_2_decryptor.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdio.h>
#include <windows.h>
#include <wincrypt.h>
#include <tchar.h>
#include <conio.h>
#include <fstream>
#include <iostream>

using namespace std;

int main(int argc, _TCHAR* argv[])
{
	HCRYPTPROV h_crypt_prov;
	HCRYPTHASH h_hash;
	HCRYPTKEY h_key;
	const char *file_name = "C:\\users\\tim\\desktop\\briefcase\\2.txt";
	
	/* Open the encrypted file */
	ifstream mySource;
	char *file_buff;
	int file_size;

	/* Open at the end so we can get the size */
	mySource.open(file_name, ios_base::binary | ios::in | ios::ate);
	file_size = mySource.tellg();

	/* Allocate and zero memory */
	file_buff = new char[file_size];
	memset(file_buff, 0,sizeof(file_buff));

	mySource.seekg(0, ios_base::beg);
	mySource.read(file_buff, file_size);
	mySource.close();
	cout << file_buff << "\n Size = " << file_size << "\n";

	//First call @0040109D
	if (CryptAcquireContext(&h_crypt_prov, NULL, NULL, PROV_RSA_AES, 0))
		printf("[+] Got context 0x%x [+]\n", h_crypt_prov);
	else
		return 1;
	//key
	const char *ascii_key = "thosefilesreallytiedthefoldertogether";
	
	//call to create hash @004011AC
	if (CryptCreateHash(h_crypt_prov, CALG_SHA1, 0, 0, &h_hash))
		printf("[+] Created hash object [+]\n");
	else
		return 1;

	//call to hash data @004011D4
	if (CryptHashData(h_hash, (BYTE *)ascii_key, strlen(ascii_key), 0))
		printf("[+] Added data to hash [+]\n");

	if (CryptDeriveKey(h_crypt_prov, CALG_AES_256, h_hash, CRYPT_EXPORTABLE, &h_key))
		printf("[+] Got Key [+]\n");

	CryptDestroyHash(h_hash);
	printf("---- %d \n", file_size);
	/* Get key len */
	DWORD key_len, val_len;
	CryptGetKeyParam(h_key, KP_KEYLEN, (LPBYTE)&key_len, &val_len, 0);
	//key_len = (key_len + 7) / 8;
	DWORD len = (DWORD)file_size;
	
	if (CryptEncrypt(h_key, NULL, true, 0, (BYTE *)file_buff, &len, len))
		printf("[+] encrypted data [+]\n");

	printf("%d\n%s\n", len, file_buff);
	
	if (CryptDecrypt(h_key, NULL, false, 0, (BYTE *)file_buff, &len))
		printf("[+] Decrypted data [+]\n");

	printf("%s\n", file_buff);
	return 0;
}

