// challenge_2_decryptor.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdio.h>
#include <windows.h>
#include <wincrypt.h>

int main()
{
	HCRYPTPROV h_crypt_prov;
	HCRYPTHASH h_hash;
	HCRYPTKEY h_key;

	//First call @0040109D
	if (CryptAcquireContext(&h_crypt_prov, NULL, NULL, PROV_RSA_AES, 0))
		printf("[+] Got context 0x%x [+]\n", h_crypt_prov);
	else
		return 1;

	//key
	char *ascii_key = "thosefilesreallytiedthefoldertogether";

	//call to create hash @004011AC
	if (CryptCreateHash(h_crypt_prov, CALG_SHA1, 0, 0, &h_hash))
		printf("[+] Created hash object [+]\n");
	else
		return 1;

	//call to hash data @004011D4
	if (CryptHashData(h_hash, (BYTE *)ascii_key, sizeof(ascii_key), 0))
		printf("[+] Added data to hash [+]\n");

	if (CryptDeriveKey(h_crypt_prov, CALG_AES_256, h_hash, CRYPT_EXPORTABLE, &h_key))
		printf("[+] Got Key [+]\n");

	BYTE pbData[16];

	if (CryptSetKeyParam(h_key, 4, pbData, 0));
	printf("[+] Set Key IV: pbData = %d [+]\n", *pbData);

	//destory the hash
	CryptDestroyHash(h_hash);

	DWORD data_len = 4;
	if (CryptGetKeyParam(h_key, KP_BLOCKLEN, pbData, &data_len, 0))
		printf("[+] Got Block Length %d [+]\n", *pbData);

	*pbData = *pbData >> 3;

	//malloc(*pbData), memset(malloc, 0, *pbData)

	//Create an md5 hash obj
	if (CryptCreateHash(h_crypt_prov, CALG_MD5, 0, 0, &h_hash))
		printf("[+] Created MD5 Hash object [+]\n");

	char *filename = "2.txt";

	if (CryptHashData(h_hash, (BYTE *)filename, 5, 0))
		printf("[+] Hashed filename [+]\n");

	//Need to figure this step out as it isnt clear
	//if(CryptSetKeyParam(h_key, 1, ))
	return 0;
}

