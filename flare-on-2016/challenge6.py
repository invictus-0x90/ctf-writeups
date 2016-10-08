#Embedded file name: poc.py
import sys, random
__version__ = 'Flare-On ultra python obfuscater 2000'
target = 5
count = 1
error_input = ''
while True:
    print '(Guesses: %d) Pick a number between 1 and 100:' % count,
    input = sys.stdin.readline()
    try:
        input = int(input, 0)
    except:
        error_input = input
        print 'Invalid input: %s' % error_input
        continue

    if target == input:
        break
    if input < target:
        print 'Too low, try again'
    else:
        print 'Too high, try again'
    count += 1

if target == input:
    win_msg = 'Wahoo, you guessed it with %d guesses\n' % count
    sys.stdout.write(win_msg)
if count > 25:
    print 'Status: took too long %d' % count
    sys.exit(1)
else:
    print 'Status: %d guesses' % count
if count > 0:
    tmp = '312a232f272e27313162322e372548'
    #tmp = ''.join((chr(ord(x) ^ 66) for x in error_input)).encode('hex')
    #if tmp != '312a232f272e27313162322e372548':
    #    sys.exit(0)
    stuffs = [67,
     139,
     119,
     165,
     232,
     86,
     207,
     61,
     79,
     67,
     45,
     58,
     230,
     190,
     181,
     74,
     65,
     148,
     71,
     243,
     246,
     67,
     142,
     60,
     61,
     92,
     58,
     115,
     240,
     226,
     171]
    import hashlib
    y = 0
    while y < 100:
        win_msg = 'Wahoo, you guessed it with %d guesses\n' % y
        stuffer = hashlib.md5(win_msg + tmp).digest()
        final = ''
        y = y + 1
    
        for x in range(len(stuffs)):
            final  += ''.join(chr(stuffs[x] ^ ord(stuffer[x % len(stuffer)])))
            print chr(stuffs[x] ^ ord(stuffer[x % len(stuffer)])),

        print

        #tmp = ''
        #for x in range(len(final)):
        #    print chr(ord(final[x]) ^ ord(stuffer[x % len(stuffer)])),
