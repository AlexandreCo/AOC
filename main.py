import re
from enum import Enum
from array import *



def isWinningNumbers(var,numbers):


    for number in numbers:

        if(int(number)==int(var)):
            return True
    return False

if __name__ == '__main__':

    file = open('./4.txt', "r")
    lines = file.readlines()
    file.close()
    sum = 0

    id=0
    for line in lines:
        line.strip()
        subline=line.strip().split("|")
        subsubline=subline[0].strip().split(":")
        cardNumbers=subsubline[1].strip().replace('  ', ' ').split(" ")
        numbers=subline[1].strip().replace('  ', ' ').split(" ")
        print(f"{cardNumbers} [",end='')
        cardvalue=0
        for number in cardNumbers:
            if(isWinningNumbers(number,numbers)):
                if(cardvalue):
                    cardvalue*=2
                else:
                    cardvalue = 1
                print(f" ({number})",end='')
            else:
                print(f" {number}", end='')
        print(f"] {cardvalue}")
        sum+=cardvalue

    print(f"result={sum}")
