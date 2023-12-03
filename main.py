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
    lblNbPartNumber = 0
    numberID=0;
    listId = []
    gearValue=1;
    def __init__(self,type,id):
        self.monType=type
        self.numberID = id

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

    def setPFalseNumber(self,id):
        self.monType=FALSE_NUMBER
        self.numberID = id
    def setPartNumber(self):
        self.monType=PART_NUMBER

    def getId(self):
        return self.numberID

    def setLabel(self,label):
        self.label=label
    def getLabel(self):
        return self.label

    def labelNewPartNumber(self,id,number):
        if(self.monType==LABEL):
            if((id in self.listId) == False):
                self.lblNbPartNumber+=1
                self.listId.append(id)
                self.gearValue=self.gearValue*number;
                #print(self.listId)
    def getLabelPartNumber(self):
        return self.lblNbPartNumber
    def getGearValue(self):
        gearValue=0
        if(self.monType==LABEL):
            if(self.lblNbPartNumber==2):
                return self.gearValue
        return gearValue

def display():
    for raw in range(0, MAX_RAW):
        print("|", end='')
        for col in range(0, MAX_COL):
            case=Plateau[raw][col]
            type=case.getType()

            if(type==PART_NUMBER):
                value=case.getNumber()
                print(f"Part({value:>3d})|", end='')

            else:
                if (type == NUMBER):
                    value = case.getNumber()
                    print(f"number({value:>3d})|", end='')
                else:
                    if (type == FALSE_NUMBER):
                        print(f"FN({value:>3d})|", end='')
                    else:
                        if (type == LABEL):
                            #print(case.getLabelPartNumber(), end='')
                            value=case.getLabelPartNumber()
                            geavValue=case.getGearValue()
                            print(f"label({value},{geavValue})", end='')
                        else:
                            if (type == NONE):
                                print("   |", end='')
                            else:
                                print("ERROR|", type, end='')
        print("")
    print("")
def getNumber(raw,col):
    num=Plateau[raw][col].getNumber()
    id=Plateau[raw][col].getId()
    for i in range (col+1,col+4):
        if(i>=MAX_COL):
            return num
        if(Plateau[raw][i].isNumber()):
            num=num*10+Plateau[raw][i].getNumber()
            Plateau[raw][i].setPFalseNumber(id)
        else:
            return num

    for i in range (col+1,col+4):
        if(i>=MAX_COL):
            return num
        if(Plateau[raw][i].getType()==FALSE_NUMBER):
            Plateau[raw][i].setNumber(num)

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

def isPartNumbers(raw,col,id,number):
    partNumber=False
    for raw_i in range (-1,2):
        for col_i in range(-1, 2):
            if(getCase(raw+raw_i,col+col_i)):
                if(Plateau[raw+raw_i][col+col_i].getType()==LABEL):
                    partNumber = True
                    Plateau[raw + raw_i][col + col_i].labelNewPartNumber(id,number)
    return partNumber

def numerise():
    sum=0
    current_id=0
    for raw in range(0, MAX_RAW):
        for col in range(0, MAX_COL):
            case=Plateau[raw][col]
            type=case.getType()
            if(type==NUMBER):
                num=getNumber(raw,col)
                Plateau[raw][col].setNumber(num)

def searchPartNumber():
    for raw in range(0, MAX_RAW):
        for col in range(0, MAX_COL):
            case=Plateau[raw][col]
            type=case.getType()
            if(type==NUMBER):
                id = Plateau[raw][col].getId()
                num = Plateau[raw][col].getNumber()
                if (isPartNumbers(raw, col,id,num)):
                    Plateau[raw][col].setPartNumber()

            if(type==FALSE_NUMBER):
                isPartNumbers(raw, col,id,num)

def getSum():
    sum=0
    for raw in range(0, MAX_RAW):
        for col in range(0, MAX_COL):
            value=Plateau[raw][col].getGearValue()
            sum+=value
    print(sum)

if __name__ == '__main__':

    file = open('./3.txt', "r")
    lines = file.readlines()
    file.close()
    sum = 0
    # Creates a list containing 5 lists, each of 8 items, all set to 0
    Plateau = [[0 for x in range(MAX_COL)] for y in range(MAX_RAW)]

    raw=0
    id=0
    for line in lines:
        line=line.strip()
        col=0
        for i in range(0, len(line)):
            type=line[i]
            if(line[i].isnumeric()):
                num=int(line[i])
                id+=1
                Plateau[raw][col]=Case(NUMBER,id)
                Plateau[raw][col].setNumber(num)
            else:
                if(line[i]=='.') :
                    Plateau[raw][col] = Case(NONE,0)
                else :
                    Plateau[raw][col] = Case(LABEL,0)
                    Plateau[raw][col].setLabel(line[i])
            #print(raw, col, Plateau[raw][col].getType())
            col += 1
        raw += 1

    #print(sum)
    numerise()
    searchPartNumber()
    display()
    getSum()

