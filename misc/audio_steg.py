#!/usr/bin/python
import wave
import struct, array, re

def main():
   wav = wave.open("audio_file.wav", "r")
   leng = wav.getnframes()
   binary = ""   

   for i in range(leng):
	data = wav.readframes(1) #read a frame
	current_data = struct.unpack("hh", data) #get the data, a tuple (leftChannel, rightChannel)
	temp = bin(int(current_data[i%2])) #get a byte, alternating from left channel to right channel
 	binary += temp[len(temp)-1] #get the lsb of the byte	

   data = [int(binary[x:x+8], 2) for x in range(0, len(binary), 8)] #turn the bit string into ints
   data = ''.join(chr(i) for i in data) #convert those ints to bytes
   print data


if __name__ == '__main__':
	main()
