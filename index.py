#!/usr/bin/python

import sys
from collections import Counter

INDEX_OF_COINCIDENCE = 0.072723
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
NUMBER_OF_LETTERS_PORTUGUESE = 26
PORTUGUESE_LETTER_FREQUENCIES = [14.634,1.043,3.882,4.992,12.570,1.023,1.303,0.781,6.186,0.397,0.015,2.779,4.738,4.446,9.735,2.523,1.204,6.530,6.805,4.336,3.639,1.575,0.037,0.253,0.006,0.470]

def calculateIndexOfCoincidence(frequency, lenght):
    ioc = 0
    for x in ALPHABET:
        ioc = ioc + (frequency[x] * (frequency[x]-1))
    return (ioc / (float(lenght * (lenght - 1))))

def letterFrequenciesDifference(text):
    difference = 0
    for i in range(0,NUMBER_OF_LETTERS_PORTUGUESE):
        frequency = text.count(ALPHABET[i])/len(text)
        difference = difference + (frequency-PORTUGUESE_LETTER_FREQUENCIES[i])**2
    return difference

def caesarShift(text, shift):
    code = ALPHABET[shift:] + ALPHABET[:shift]
    return text.translate({ord(x):y for (x, y) in zip(ALPHABET, code)})

def getNthLetters(text, start, n):
    value = ""
    for i in range(0,len(text)):
        if i%n == start:
            value = value+text[i]
    return value

def guessKeyLenght(encryptedText):
    keyLenght = -1
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
        if (INDEX_OF_COINCIDENCE-0.01) <= (sum(listOfIOC) / len(listOfIOC)) <= (INDEX_OF_COINCIDENCE+0.01):
            keyLenght = i
            break
    if keyLenght == -1:
        raise Exception("Não foi possivel encontrar tamanho da chave")
    return keyLenght

def guessKey(text, length):
    guess = ""
    for i in range(0, length):
        x = getNthLetters(text, i, length)
        shiftGuessed = 0
        frequency = Counter(x)
        frequency = frequency.most_common()
        for j in range(0, 3):
            shift = ALPHABET.index(frequency[j][0])
            shiftedText = caesarShift(x, -shift)
            current = letterFrequenciesDifference(shiftedText)
            if j == 0:
                shiftGuessed = shift
                smaller = current
            if current < smaller:
                shiftGuessed = shift
                smaller = current
        guess = guess+ALPHABET[shiftGuessed]
    return guess

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
    print("Utilização: python .\\index.py {File Name}")
    quit

encryptedFile = open(sys.argv[1], "r")
encryptedText = encryptedFile.read()
encryptedText = encryptedText.lower()
encryptedFile.close()

keyLenght = guessKeyLenght(encryptedText)

print("Tamanho da palvra: " + str(keyLenght))

key = guessKey(encryptedText, keyLenght)

print("Chave: " + key)

decryptedText = decryptText(keyLenght, key, encryptedText)

f = open("decryptedText.txt", "w")
f.write(decryptedText)
f.close()

print("Texto decifrado salvo em decryptedText.txt")