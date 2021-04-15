#!/usr/bin/python

import sys
from collections import Counter

INDEX_OF_COINCIDENCE = 0.072723
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
NUMBER_OF_LETTERS_PORTUGUESE_ALPHABET = 26
PORTUGUESE_LETTER_FREQUENCIES = [14.634,1.043,3.882,4.992,12.570,1.023,1.303,0.781,6.186,0.397,0.015,2.779,4.738,4.446,9.735,2.523,1.204,6.530,6.805,4.336,3.639,1.575,0.037,0.253,0.006,0.470]

def calculateIndexOfCoincidence(frequency, lenght):
    ioc = 0
    for x in ALPHABET:
        ioc = ioc + (frequency[x] * (frequency[x]-1))
    return (ioc / (float(lenght * (lenght - 1))))

def getNthLetters(text, start, n):
    value = ""
    for i in range(0,len(text)):
        if i%n == start:
            value = value+text[i]
    return value

def letterFrequencies(text):
    kr = 0
    for i in range(0,NUMBER_OF_LETTERS_PORTUGUESE_ALPHABET):
        occurences = text.count(ALPHABET[i])/len(text)
        kr = kr + (occurences-PORTUGUESE_LETTER_FREQUENCIES[i])**2
    return kr

def caesarShift(text, shift):
    code = ALPHABET[shift:] + ALPHABET[:shift]
    return text.translate({ord(x):y for (x, y) in zip(ALPHABET, code)})

def guessKey(text, length):
    guess = ""
    for i in range(0, length):
        t = getNthLetters(text, i, length)
        smaller = -1
        shift = 0
        for j in range(0, NUMBER_OF_LETTERS_PORTUGUESE_ALPHABET):
            tl = caesarShift(t, -j)
            current = letterFrequencies(tl)
            if smaller == -1:
                smaller = current
            if current < smaller:
                shift = j
                smaller = current
        guess = guess+ALPHABET[shift]
    return guess

def guessKeyLenght(encryptedText):
    for i in range(1,26):
        print("m = " + str(i))
        listOfIOC = []
        for j in range(0,i):
            text = ""
            for x in range(j, len(encryptedText)-1, i):
                text = text + encryptedText[x]
            frequency = Counter(text)
            ioc = calculateIndexOfCoincidence(frequency, len(text))
            listOfIOC.append(ioc)
        print("Indice Medio: " + str(sum(listOfIOC) / len(listOfIOC)))
        if 0.065 <= (sum(listOfIOC) / len(listOfIOC)) <= 0.085:
            keyLenght = i
            break
    return keyLenght

def groupNthLetters(keyLenght, encryptedText):
    encryptedTextList = []
    for j in range(0,keyLenght):
        text = getNthLetters(encryptedText, j, keyLenght)
        print(Counter(text))
        encryptedTextList.append(text)
    return encryptedTextList

def decryptText(keyLenght,key,encryptedText):
    shift = [0]*keyLenght
    for idx, x in enumerate(key):
        shift[idx] = ALPHABET.index(x)
    count = 0 
    clearText = ""
    for x in encryptedText:
            realLetter = caesarShift(x, -shift[count])
            clearText = clearText + realLetter
            count = (count + 1) % keyLenght
    return clearText

if len(sys.argv) < 2:
    print("Numero de argumentos incorreto")
    quit

encryptedFile = open(sys.argv[1], "r")
encryptedText = encryptedFile.read()
encryptedFile.close()

keyLenght = guessKeyLenght(encryptedText)

print("Tamanho da palvra: " + str(keyLenght))

encryptedTextList = groupNthLetters(keyLenght, encryptedText)

key = guessKey(encryptedText, keyLenght)

print("Chave: " + key)

clearText = decryptText(keyLenght, key, encryptedText)
    
f = open("clearText.txt", "w")
f.write(clearText)
f.close()