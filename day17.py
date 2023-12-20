import re
import sys

import numpy as np
from ant import *
from case import *
from debug import *
from univers import *
#pip install opencv-python
import cv2

class Path:
    def __init__(self,x,y,heatloss):
        self.x=x
        self.y=y
        self.heatloss=heatloss

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

    def displayPath(self,x,y,stop):
        self.displayU(False)
        for path in self.cases[x][y].aPath:
            self.cases[path.x][path.y].displayGrey(cv2, self.img)
        cv2.imshow('img', self.img)
        if (stop == False):
            key = cv2.waitKey(1)
        else:
            key = cv2.waitKey(0) & 0x0FF


    def addCase(self, heatloss, x, y):
        debug = self.debug
        self.cases[x][y] = Case17(debug,heatloss,x,y,self.nb_cases)
        self.nb_cases += 1

    def addWorkingCase(self,aCases,new, x, y,dir):
        #print(x,y)
        limit, x, y = self.limitXY(x, y)
        if (limit == False):
            neighbor=self.cases[x][y]
            h = new.totalHeatLoss + neighbor.heatloss
            th = neighbor.totalHeatLoss
            if (th == -1):
                if(new.dir==dir):
                    if(new.countForward>=2):
                        return
                    else:
                        neighbor.countForward = new.countForward + 1
                else:
                    neighbor.countForward = 0
                neighbor.dir=dir
                th = h
                p=new.aPath.copy()
                p.append(Path(new.x,new.y,th))
                neighbor.aPath=p
                neighbor.totalHeatLoss=th
                aCases.append(neighbor)
            else:
                if (th == -1):
                    if (new.dir == dir):
                        if (new.countForward >= 2):
                            return
                        else:
                            neighbor.countForward = new.countForward + 1
                    else:
                        neighbor.countForward = 0
                    neighbor.dir = dir
                    th = h
                    p = new.aPath.copy()
                    p.append(Path(new.x, new.y, th))
                    neighbor.aPath = p
                    neighbor.totalHeatLoss = th
                    aCases.append(neighbor)

    def getLowest(self):
        aC=self.aCases
        self.aCases=[]
        cMin = aC.pop(0)
        for case in aC:
            if(cMin.totalHeatLoss > case.totalHeatLoss):
                # smaller
                self.aCases.append(cMin)
                cMin=case
            else:
                self.aCases.append(case)
        return cMin




    def start(self,x,y,dir):
        self.aCases=[]
        self.cases[x][y].totalHeatLoss=self.cases[x][y].heatloss
        self.cases[x][y].dir=dir
        self.cases[x][y].countForward=1
        self.aCases.append(self.cases[x][y])

        self.displayU(False)
        while len(self.aCases):
            new=self.getLowest()
            x,y=new.getNorth()
            self.addWorkingCase(self.aCases,new,x,y,'n')
            x,y=new.getWest()
            self.addWorkingCase(self.aCases,new,x,y,'w')
            x,y=new.getEast()
            self.addWorkingCase(self.aCases,new,x,y,'e')
            x,y=new.getSouth()
            self.addWorkingCase(self.aCases,new,x,y,'s')
            self.displayU(False)
            #self.displayPath(new.x,new.y,False)

        x=self.init_x_max
        y=self.init_y_max
        self.displayPath(x,y, True)


        return self.cases[x][y].totalHeatLoss
class Case17(Case):
    def __init__(self, debug, heatloss, x, y, num):
        Case.__init__(self, debug, heatloss, x, y, num,cCaseWidth,cCaseHeight)
        self.heatloss=int(heatloss)
        self.totalHeatLoss=-1
        self.aPath = []
        self.countForward=0
        self.dir='x';

    def display(self, cv2, img):
        color=(int(self.heatloss) * 25, 0, 0)
        self.cv2DisplayBack(cv2, img,color)
        if(self.cCaseWidth>35):
            self.cv2DisplayCenter(cv2, img,str(self.totalHeatLoss))
        if (self.cCaseWidth >= 70):
            self.cv2DisplayNorth(cv2, img,str(self.heatloss))
            self.cv2DisplaySouth(cv2, img,str(self.heatloss))
            self.cv2DisplayEast(cv2, img,str(self.heatloss))
            self.cv2DisplayWest(cv2, img, str(self.heatloss))

    def displayGrey(self, cv2, img):
        color=(0xD9, 0xD9, 0xD9)
        self.cv2DisplayBack(cv2, img,color)
        if(self.cCaseWidth>=70):
            self.cv2DisplayNorth(cv2, img,str(self.totalHeatLoss))
            self.cv2DisplaySouth(cv2, img,str(self.heatloss))

coef=10
cCaseWidth=7*coef
cCaseHeight=7*coef


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
    univers.displayU(True)
    result=univers.start(1,0,'e')
    return result


if __name__ == '__main__':
    debug = eVisulvl
    filename = './17-tiny.txt'
    part = 1

    print(f"Part 1 : {runpart(debug,1)}")
    #print(f"Part 2 : {runpart(debug,2)}")



