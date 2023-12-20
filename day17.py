import re
import sys

import numpy as np
from ant import *
from case import *
from debug import *
from univers import *
#pip install opencv-python
import cv2



class Univers17(Univers):

    def __init__(self, debug, init_x_max, init_y_max,cases,cCaseWidth,cCaseHeight):
        Univers.__init__(self,debug,init_x_max, init_y_max ,cases )
        self.img = np.zeros((self.init_x_max*cCaseHeight, self.init_y_max*cCaseWidth, 3), np.uint8)
        self.stepByStep=False
        self.cCaseWidth=cCaseWidth
        self.cCaseWidth = cCaseHeight

    def displayU(self, stop):
        mx=self.init_x_max+1
        my=self.init_y_max+1
        self.img = np.zeros((mx * cCaseHeight, my * cCaseWidth, 3), np.uint8)
        for y in range(0, my):
            for x in range(0, mx):
                self.cases[x][y].display(cv2,self.img)
        cv2.imshow('img', self.img)
        if (stop == False):
            key = cv2.waitKey(1)
        else:
            key = cv2.waitKey(0) & 0x0FF

    def addCase(self, heatloss, x, y):
        debug = self.debug
        self.cases[x][y] = Case17(debug,heatloss,x,y,self.nb_cases)
        self.nb_cases += 1

    def addWorkingCase(self,aCase,new, x, y):
        print(x,y)
        limit, x, y = self.limitXY(x, y)
        if (limit == False):
            neighbor=self.cases[x][y]
            h = new.totalHeatLoss + new.heatloss
            th = neighbor.totalHeatLoss
            if (th == -1):
                th = h
                neighbor.totalHeatLoss=th
                aCase.append(neighbor)
            else:
                if (h < th):
                    th = h
                    neighbor.totalHeatLoss = th
                    aCase.append(neighbor)

    def start(self,x,y):
        aCase=[]
        self.cases[x][y].totalHeatLoss=0
        aCase.append(self.cases[x][y])
        self.displayU(True)
        while len(aCase):
            new=aCase.pop(0)
            x,y=new.getEast()
            self.addWorkingCase(aCase,new,x,y)
            x,y=new.getSouth()
            self.addWorkingCase(aCase,new,x,y)
            x,y=new.getWest()
            self.addWorkingCase(aCase,new,x,y)
            x,y=new.getNorth()
            self.addWorkingCase(aCase,new,x,y)

        self.displayU(True)

class Case17(Case):
    def __init__(self, debug, heatloss, x, y, num):
        Case.__init__(self, debug, heatloss, x, y, num,cCaseWidth,cCaseHeight)
        self.heatloss=int(heatloss)
        self.totalHeatLoss=-1

    def display(self, cv2, img):
        color=(int(self.heatloss) * 25, 0, 0)
        self.cv2DisplayBack(cv2, img,color)
        self.cv2DisplayCenter(cv2, img,str(self.totalHeatLoss))
        self.cv2DisplayNorth(cv2, img,str(self.heatloss))
        self.cv2DisplaySouth(cv2, img,str(self.heatloss))
        self.cv2DisplayEast(cv2, img,str(self.heatloss))
        self.cv2DisplayWest(cv2, img, str(self.heatloss))




coef=8
cCaseWidth=9*coef
cCaseHeight=9*coef


def isDebug(debug, lvl):
    if (debug >= lvl):
        return True
    else:
        return False


def getUniversSize(lines):
    y_max = 0
    for line in lines:
        x_max = len(line.strip())
        y_max += 1
    return x_max,y_max

def getData(filename, part, debug):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()


    j = 0
    x_max,y_max=getUniversSize(lines)

    print(x_max,y_max)

    univers = Univers17(debug,
                        x_max-1, y_max-1,
                        np.array([[0 for x in range(y_max + 1)] for y in range(x_max + 1)], dtype=Case17),
                        cCaseWidth,cCaseHeight)


    y = 0
    for line in lines:
        x = 0
        for x, heatloss in enumerate(line.strip()):
            if isDebug(debug, eDbglvl):
                print(f"[{x},{y} : {heatloss} ]", end="")
            univers.addCase(heatloss,x, y)

        if isDebug(debug, eDbglvl):
            print(f"")
        y += 1
    return univers


def runpart(debug, part):
    result = 0
    univers = getData(filename, part, debug)

    univers.start(1,0)
    return result


if __name__ == '__main__':
    debug = eVisulvl
    filename = './17-tiny.txt'
    part = 1

    print(f"Part 1 : {runpart(debug,1)}")
    #print(f"Part 2 : {runpart(debug,2)}")



