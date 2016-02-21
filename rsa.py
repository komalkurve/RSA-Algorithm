from random import randint

EOptions = [3, 5, 17, 257, 65537]
ELength = len(EOptions)

def IsFermatPrime(number):

    ''' fermat primality check '''
    if (number > 1):
        for time in range(3):
            randomNumber = randint(2, number)-1
            ''' (Test if a^(n-1) = 1 mod n '''
            if (pow(randomNumber,number-1,number) != 1):
                return False

        return True
    else:
        return False

def getPrime(bitLength):

    '''maximum  and minimum number possible with length equal to bit length'''
    minValue = (2 ** (bitLength - 1)) + (2 ** (bitLength-2)) + 1
    maxStringList = ['1'] * bitLength
    maxString = ''.join(maxStringList)
    maxValue = int(maxString, 2)
    while True:
        randNumber = randint(minValue, maxValue)
        #print randNumber
        if IsFermatPrime(randNumber):
              return randNumber
              ''''returns prime number'''
        #print "going on"

def modInv(publicMod,phi):
     '''to find mod inverse that is to find private key'''
     t = 0
     r = phi
     newt = 1
     newr = publicMod
     while newr != 0:
         quotient = r / newr
         t, newt = newt, t - quotient * newt
         r, newr = newr, r - quotient * newr
         #print t, r
     if t < 0:
         t = t + phi
     if r > 1:
         raise RuntimeError("publicMod is not invertible")
     return t

def getPair(bitLength):
    '''returns public key,private key and modulus n'''
    index = randint(0,ELength-1)
    publicMod = EOptions[index]

    while True:
        firstPrime = getPrime(bitLength/2)
        #print "first %d, %d " %(firstPrime, publicMod)
        if firstPrime % publicMod != 1:
            break

    while True:
        secondPrime = getPrime(bitLength/2)
        #print "second %d, %d" %(secondPrime, publicMod)
        if secondPrime % publicMod != 1 and secondPrime != firstPrime:
            break

    prod = firstPrime * secondPrime
    phi = (firstPrime - 1) * (secondPrime - 1)

    try:
        privateMod = modInv(publicMod, phi)
        return (prod, publicMod, privateMod)
    except RuntimeError as e:
        print e



def encrypt(text, n, e):
    cipherText = ""
    stringLength = len(text)
    for i in range(0,stringLength):
        temp = ord(text[i])
        temp = pow(temp, e, n)
        cipherText = cipherText + str(temp) + 'c'
        #print "in encrypt %s" %(cipherText)
    return cipherText


def decipher(number,n,d):
    temp = pow(number, d, n)
    return chr(temp)


def decrypt(cipherText, n, d):
    decipheredText = ''
    character = ''

    for char in cipherText:
            if char == 'c' or char == 'e':
                decipheredText += decipher(int(character),n,d)
                character = ''
            else:
                character += char
    return decipheredText
