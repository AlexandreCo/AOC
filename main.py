import re
from enum import Enum
from array import *

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

Color = Enum('Color', ['RED', 'GREEN', 'BLUE'])
def spelledToNumber(line):
    line = line.replace(str("one"), "o1")
    line = line.replace(str("two"), "t2")
    line = line.replace(str("three"), "t3")
    line = line.replace(str("four"), "f4")
    line = line.replace(str("five"), "f5")
    line = line.replace(str("six"), "s6")
    line = line.replace(str("seven"), "s7")
    line = line.replace(str("eight"), "e8")
    line = line.replace(str("nine"), "n9")
    return line

def spelledToNumberRevers(line):
    line = line.replace(str("one")[::-1], "e1")
    line = line.replace(str("two")[::-1], "o2")
    line = line.replace(str("three")[::-1], "e3")
    line = line.replace(str("four")[::-1], "r4")
    line = line.replace(str("five")[::-1], "e5")
    line = line.replace(str("six")[::-1], "x6")
    line = line.replace(str("seven")[::-1], "n7")
    line = line.replace(str("eight")[::-1], "t8")
    line = line.replace(str("nine")[::-1], "e9")
    return line


def removeLetter(line) :
    return re.sub("[a-z]", "", line)


NONE=" "
NUMBER=1
LABEL="*"
FALSE_NUMBER=3
PART_NUMBER=4

MAX_RAW=140
MAX_COL=140

class Case:
    monType=NONE
    number=0
    label=False
    def __init__(self,type):
        self.monType=type

    def getType(self):
        return self.monType
    def getNumber(self):
        return self.number

    def isNumber(self):
        if(self.monType==NUMBER):
            return True
        else:
            return False
    def setNumber(self,num):
        self.number=num
    def changeType(self,type):
        self.monType=type
    def setLabel(self,label):
        self.label=label
    def getLabel(self):
        return self.label

def display():
    for raw in range(0, MAX_RAW):
        for col in range(0, MAX_COL):
            case=Plateau[raw][col]
            type=case.getType()
            if(type==PART_NUMBER):
                print(case.getNumber(), end='')
            else:
                if (type == NUMBER):
                    num=case.getNumber()
                    if(num<10):
                        print('X', end='')
                    else:
                        if (num < 100):
                            print('XX', end='')
                        else:
                            if (num < 1000):
                                print('XXX', end='')
                            else:
                                print('XXXX', end='')
                else:
                    if (type == FALSE_NUMBER):
                        print("", end='')
                    else:
                        if (type == LABEL):
                            print(case.getLabel(), end='')
                        else:
                            if (type == NONE):
                                print(" ", end='')
                            else:
                                print("ERROR", type, end='')
        print("")
    print("")
def getNumber(raw,col):
    num=Plateau[raw][col].getNumber()

    for i in range (col+1,col+4):
        if(i>=MAX_COL):
            return num
        if(Plateau[raw][i].isNumber()):
            num=num*10+Plateau[raw][i].getNumber()
            Plateau[raw][i].changeType(FALSE_NUMBER)
            Plateau[raw][i].setNumber(0)
            if (isPartNumbers(raw,i)):
                Plateau[raw][col].changeType(PART_NUMBER)
        else:
            return num
    return num


def getCase(raw,col):

    if(raw<0):
        return False
    if(raw>=MAX_RAW):
        return False
    if(col<0):
        return False
    if(col>=MAX_COL):
        return False
    return True

def isPartNumbers(raw,col):
    partNumber=False

    for raw_i in range (-1,2):
        for col_i in range(-1, 2):
            if(getCase(raw+raw_i,col+col_i)):
                if(Plateau[raw+raw_i][col+col_i].getType()==LABEL):
                    partNumber = True
    return partNumber

def numerise():
    sum=0
    for raw in range(0, MAX_RAW):
        for col in range(0, MAX_COL):
            case=Plateau[raw][col]
            type=case.getType()
            if(type==NUMBER):
                num=getNumber(raw,col)
                Plateau[raw][col].setNumber(num)
                if (isPartNumbers(raw, col)):
                    Plateau[raw][col].changeType(PART_NUMBER)
    sum+=Plateau[raw][col].getNumber()
    print(sum)

def getSum():
    sum=0
    for raw in range(0, MAX_RAW):
        for col in range(0, MAX_COL):
            if(Plateau[raw][col].getType()==PART_NUMBER):
                sum+=Plateau[raw][col].getNumber()
    print(sum)

if __name__ == '__main__':

    file = open('./3.txt', "r")
    lines = file.readlines()
    file.close()
    sum = 0
    # Creates a list containing 5 lists, each of 8 items, all set to 0
    Plateau = [[0 for x in range(MAX_COL)] for y in range(MAX_RAW)]

    raw=0
    for line in lines:
        line=line.strip()
        col=0
        for i in range(0, len(line)):
            type=line[i]
            if(line[i].isnumeric()):
                num=int(line[i])
                Plateau[raw][col]=Case(NUMBER)
                Plateau[raw][col].setNumber(num)
            else:
                if(line[i]=='.') :
                    Plateau[raw][col] = Case(NONE)
                else :
                    Plateau[raw][col] = Case(LABEL)
                    Plateau[raw][col].setLabel(line[i])
            #print(raw, col, Plateau[raw][col].getType())
            col += 1
        raw += 1

    #print(sum)
    numerise()
    display()
    getSum()