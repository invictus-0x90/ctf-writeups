import hashlib
import binascii
import base64
import struct
from ecdsa import NIST192p, SigningKey, keys, NIST384p, numbertheory
import ecdsa

def convert_to_int(signature):
	s = base64.b64decode(signature) #decode the string back to raw
	num = int(binascii.hexlify(s), 16) #convert the raw bytes to an int
	return num


original = "BRXVEpTGwCo1HsaTNmhJ5NynvUsdhFzvc1ilypdV4aDLRLIlVaCCkHsuN6EAet0+"
#m_1 corresponds to s_1 and the same goes for m_2
m_1 = "iSsuZJOq1FNKMuK4wm88UEkr21wgsypW" 
m_2 = "x3wqOnaetBPO66TrBaMyr3NQIDbhvK0w"

z_1 = int(binascii.hexlify(hashlib.sha1(m_1).digest()), 16)
z_2 = int(binascii.hexlify(hashlib.sha1(m_2).digest()), 16)

s_1 = convert_to_int("c1ilypdV4aDLRLIlVaCCkHsuN6EAet0+")         
s_2 = convert_to_int("SvNuLoc421+3BZMMFukNTOztlpj9kf4e")
r = convert_to_int("BRXVEpTGwCo1HsaTNmhJ5NynvUsdhFzv")

order = NIST192p.order

#The following calculations are based on the explanation in https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm
#It took a while to figure out that where the writer had put a = b/c, he really meant a = b * inversemod(c, order) mod order
k_1 = (z_1 - z_2) * numbertheory.inverse_mod((s_1 - s_2), order) % order 

d_A = (s_1*k_1 - z_1) * numbertheory.inverse_mod(r, order) % order

priv_key = ecdsa.SigningKey.from_secret_exponent(d_A)

#test with pcap sigs
sig = priv_key.sign(m_1, k=k_1)
sig = base64.b64encode(sig)
print sig
print original

#nonce from server
sig = priv_key.sign("wOi3CWK6p6TM4aqcg2KcTFhNhjKGeoOY")
sig = base64.b64encode(sig)

print sig
