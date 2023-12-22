import re
import sys

import numpy as np
from ant import *
from case import *
from debug import *
from univers import *
#pip install opencv-python
# 1238
#
import cv2

class Path:
    def __init__(self,x,y,z,d,heatloss):
        self.x=x
        self.y=y
        self.z=z
        self.d = d
        self.heatloss=heatloss


class Univers17(Univers):

    def __init__(self, debug, init_x_max, init_y_max,cases,cCaseWidth,cCaseHeight):
        Univers.__init__(self,debug,init_x_max, init_y_max ,cases )
        self.init_z_max=4
        self.init_d_max=2


        #self.img = np.zeros((self.init_x_max*cCaseHeight, self.init_y_max*cCaseWidth, 3), np.uint8)
        self.img = np.zeros((self.init_x_max * cCaseHeight, self.init_y_max * cCaseWidth, 3), np.uint8)
        self.stepByStep=False
        self.cCaseWidth=cCaseWidth
        self.cCaseWidth = cCaseHeight

    def displayU(self, stop):
        mx=self.init_x_max+1
        my=self.init_y_max+1
        self.img = np.zeros((my * cCaseWidth, mx * cCaseHeight,  3), np.uint8)
        for y in range(0, my):
            for x in range(0, mx):
                self.cases[x][y][0][0].display(cv2,self.img)
        cv2.imshow('img', self.img)
        if (stop == False):
            key = cv2.waitKey(1)
        else:
            key = cv2.waitKey(0) & 0x0FF

    def displayPath(self,x,y,stop,dir,z):
        self.displayU(False)
        case=self.getCase(x,y,z,dir)
        for path in case.aPath:
            c=self.getCase(path.x,path.y,path.z,path.dir)
            c.displayGrey(cv2, self.img)
        case.displayGrey(cv2, self.img)
        cv2.imshow('img', self.img)
        if (stop == False):
            key = cv2.waitKey(1)
        else:
            key = cv2.waitKey(0) & 0x0FF

    def printAll(self):
        mx=self.init_x_max+1
        my=self.init_y_max+1
        for y in range(0, my):
            for xn in range(0, mx):
                th=self.casesNS[xn][y].totalHeatLoss
                h=self.casesNS[xn][y].heatloss
                print("[{0:d}] {1:2d} | ".format(h,th), end="")
            print("     #       ",end="")
            for xe in range(0, mx):
                th=self.casesEW[xe][y].totalHeatLoss
                h=self.casesEW[xe][y].heatloss
                print("[{0:d}] {1:2d} | ".format(h,th), end="")
            print("")
        print("")

    def printAllDir(self):
        mx = self.init_x_max + 1
        my = self.init_y_max + 1
        for y in range(0, my):
            for x in range(0, mx):
                print("[{0}] | ".format(self.casesNS[x][y].nativedir), end="")
            print("     #       ", end="")
            for x in range(0, mx):
                print("[{0}] | ".format(self.casesEW[x][y].nativedir), end="")
            print("")
        print("")
    def addCase(self, heatloss, x, y):
        debug = self.debug
        for z in range(0,4):
            for d in range(0, 4):
                self.cases[x][y][z][d] = Case17(debug,heatloss,x,y,z,d,self.nb_cases)

        self.nb_cases += 1

    def setTotalHeatLoss(self,x,y,z,d,totalHeatLoss):
        self.cases[x][y][z][d].totalHeatLoss = totalHeatLoss


    def getNbF(self,case):

        if(len(case.aPath)==0):
            return 0
        if(len(case.aPath)==1):
            return 0
        if(len(case.aPath)==2):
            if(case.aPath[-1]==case.aPath[-2]):
                return 1
            else:
                return 0

        if(len(case.aPath)==3):
            if (case.aPath[-1] == case.aPath[-2]):
                if (case.aPath[-2] == case.aPath[-3]):
                    return 2
                else:
                    return 1
            else:
                return 0

        if (case.aPath[-1] == case.aPath[-2]):
            if (case.aPath[-2] == case.aPath[-3]):
                if (case.aPath[-3] == case.aPath[-4]):
                    return 3
                else:
                    return 2
            else:
                return 1
        else:
            return 0

        return 0

    def limitXYZ(self,x,y,z):
        limit,x,y=Univers.limitXY(self,x,y)
        if (z > self.init_z_max):
            z = self.init_z_max
            limit = True
        if (z < 0 ):
            z = 0
            limit = True
        return limit,x,y,z

    def addWorkingCase(self,aCases,new, x, y, z, d):

        limit, x, y , z = self.limitXYZ(x, y , z)
        if (limit == False):
            neighbor=self.getCase(x,y,z,d)
            h = new.totalHeatLoss + neighbor.heatloss
            th = neighbor.totalHeatLoss
            if (th > h):
                th = h
                p = new.aPath.copy()
                p.append(Path(new.x,new.y,new.z,dir,th))
                neighbor.aPath = p
                self.setTotalHeatLoss(neighbor.x,neighbor.y,neighbor.z,neighbor.d,th)
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


    def getCase(self,x,y,z,d):
        print("GC : ",x,y,z,d)
        if(d==4):
            print("error")
        return self.cases[x][y][z][d]


    def start(self,x,y,z,d,max_forward):
        self.aCases=[]
        print("S=>", x, y, z, d)
        case=self.getCase(x,y,z,d)

        case.aPath.append(Path(x, y, z, d,0))

        self.setTotalHeatLoss(x, y, z, d, 0)

        #case.dir=dir
        self.aCases.append(case)

        while len(self.aCases):
            new=self.getLowest()
            print("N=>",new.x,new.y,new.z,new.d)
            x,y,z,d=new.getForward()

            print("F=>",x, y, z, d)
            self.addWorkingCase(self.aCases,new,x,y,z,d)

            x,y,z,d=new.getRight()
            print("R=>", x, y, z, d)
            self.addWorkingCase(self.aCases,new,x,y,z,d)

            x,y,z,d=new.getLeft()
            print("L=>", x, y, z, d)
            self.addWorkingCase(self.aCases,new,x,y,z,d)
            print("")


        xfinal=self.init_x_max
        yfinal=self.init_y_max
        for z in range (0,4):
            print("n:",self.getCase(xfinal, yfinal, z, cCaseNorth).totalHeatLoss)
            print("e:",self.getCase(xfinal, yfinal,  z, cCaseEast).totalHeatLoss)
            self.displayPath(xfinal, yfinal, True, cCaseEast,z)
        #self.displayPath(xfinal, yfinal, True, cCaseNorth)
        return 0
class Case17(Case):
    def __init__(self, debug, heatloss, x, y, z,d,num):
        Case.__init__(self, debug, heatloss, x, y, num,cCaseWidth,cCaseHeight)
        self.heatloss=int(heatloss)
        self.totalHeatLoss=10000
        self.aPath = []
        self.z=z
        self.d = d
        if(d==cCaseNorth):
            self.dx = 0
            self.dy = -1
        if(d==cCaseEast):
            self.dx = 1
            self.dy = 0
        if(d==cCaseSouth):
            self.dx = 0
            self.dy = 1
        if(d==cCaseWest):
            self.dx = -1
            self.dy = -0
    def display(self, cv2, img):
        color=(255-int(self.heatloss)*25, 0, 0)
        self.cv2DisplayBack(cv2, img,color)
        if(self.totalHeatLoss>-1):
            if (self.cCaseWidth >= 70):
                self.cv2DisplayWest(cv2, img, str(self.heatloss) + "/" + str(self.totalHeatLoss))
            else:
                if(self.cCaseWidth>35):
                    self.cv2DisplayCenter(cv2, img,str(self.totalHeatLoss))

    def displayGrey(self, cv2, img):
        color=(0xD9, 0xD9, 0xD9)
        self.cv2DisplayBack(cv2, img,color)
        if (self.cCaseWidth >= 70):
            self.cv2DisplayWest(cv2, img, str(self.heatloss) + "/" + str(self.totalHeatLoss))
        else:
            if(self.cCaseWidth>35):
                self.cv2DisplayCenter(cv2, img,str(self.totalHeatLoss))

    def getTotalHeatLoss(self,dir):
        self.totalHeatLoss

    def getForward(self):
        x=self.x+self.dx
        y=self.y+self.dy
        z=self.z+1
        d=self.d
        return x,y,z,d

    def getBackward(self):
        x = self.x - self.dx
        y = self.y - self.dy
        z = self.z + 1
        d = self.d
        return x, y, z, d

    def getRight(self):
        x=self.x+self.dx
        y=self.y+self.dy
        z=0
        d=self.d+1
        if(d==4):
            d=0
        return x, y, z, d

    def getLeft(self):
        x=self.x+self.dx
        y=self.y+self.dy
        z=0
        d=self.d-1
        if(d==-1):
            d=3
        return x, y, z, d



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

def getData(filename, part, debug,max_forward):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    j = 0
    x_max,y_max=getUniversSize(lines)
    univers = Univers17(debug,
                        x_max-1, y_max-1,
                        np.array([[[[0 for d in range(cCaseMaxDir)] for z in range(max_forward+1)] for y in range(y_max + 1)] for x in range(x_max + 1)], dtype=Case17),
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
    result = 0
    max_forward=3
    univers = getData(filename, part, debug,max_forward)
    #univers.printAllDir()
    #univers.displayU(True)
    result=univers.start(0,0,0,cCaseEast,max_forward)
    return result


if __name__ == '__main__':
    debug = eVisulvl
    filename = './17-tiny.txt'
    part = 1

    print(f"Part 1 : {runpart(debug,1)}")
    #print(f"Part 2 : {runpart(debug,2)}")



