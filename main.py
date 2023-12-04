import re
from enum import Enum
from array import *

debug=0
def isWinningNumbers(var,numbers):


    for number in numbers:

        if(int(number)==int(var)):
            return True
    return False


def getCardNumbers(lines,numcard):

    line=lines[numcard]
    subline = line.strip().split("|")
    subsubline = subline[0].strip().split(":")
    cardNumbers = subsubline[1].strip().replace('  ', ' ').split(" ")
    return cardNumbers

def getCardName(lines,numcard):
    line=lines[numcard].strip()
    subline = line.strip().split("|")
    subsubline = subline[0].strip().split(":")
    cardName = subsubline[0].strip()
    return cardName

def getNumbers(lines,numcard):
    line=lines[numcard].strip()
    subline = line.strip().split("|")
    subsubline = subline[0].strip().split(":")
    numbers = subline[1].strip().replace('  ', ' ').split(" ")
    return numbers

def pickCard(lines,numCard):
    global nbTotalPickCard
    cardNumbers = getCardNumbers(lines,numCard)
    numbers = getNumbers(lines,numCard)
    name = getCardName(lines,numCard)
    match = 0
    if (debug):
        print(f"{name} [", end='')
    nbTotalPickCard += 1
    for number in cardNumbers:
        if (isWinningNumbers(number, numbers)):
            match+=1
            if (debug):
                print(f" ({number})", end='')
        else:
            if (debug):
                print(f" {number}", end='')
    if (debug):
        print(f"] match={match} total : {nbTotalPickCard}")

    return match


def getCopy(lines,numCard,match):
    for i in range(numCard+1, match + numCard+1):
        name = getCardName(lines, i)
        if (debug>1):
            print(f"New Copy : idx {i} {name}")
        testPickCard(lines,i)


def testPickCard(lines,numCard):
    name=getCardName(lines,numCard)
    if (debug>1):
        print(f"testPick : {name} ({numCard}),")
    if (debug):
        print("{")
    match = pickCard(lines,numCard)
    if (match):
        getCopy(lines, numCard, match)
    if (debug):
        print("}")

nbTotalPickCard = 0
if __name__ == '__main__':

    file = open('./4.txt', "r")
    lines = file.readlines()
    file.close()
    sum = 0

    id=0

    numCard=0
    for line in lines:
        testPickCard(lines,numCard)
        numCard+=1

    print(nbTotalPickCard)



