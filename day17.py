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
        self.x = x
        self.y = y
        self.z = z
        self.d = d
        self.heatloss=heatloss


class Univers17(Univers):

    def __init__(self, debug, x_max, y_max,z_max,d_max,cases,cCaseWidth,cCaseHeight):
        Univers.__init__(self,debug,x_max, y_max ,cases )
        self.z_max=z_max
        self.d_max=d_max


        #self.img = np.zeros((self.x_max*cCaseHeight, self.y_max*cCaseWidth, 3), np.uint8)
        self.img = np.zeros((self.x_max * cCaseHeight, self.y_max * cCaseWidth, 3), np.uint8)
        self.stepByStep=False
        self.cCaseWidth=cCaseWidth
        self.cCaseWidth = cCaseHeight

    def displayU(self, stop):
        mx=self.x_max
        my=self.y_max
        self.img = np.zeros((my * cCaseWidth, mx * cCaseHeight,  3), np.uint8)
        for y in range(0, my):
            for x in range(0, mx):
                self.cases[x][y][0][0].display(cv2,self.img)
        cv2.imshow('img', self.img)
        if (stop == False):
            key = cv2.waitKey(1)
        else:
            key = cv2.waitKey(0) & 0x0FF

    def displayPath(self,x,y,z,d,stop):
        self.displayU(False)
        case=self.getCase(x,y,z,d)
        for path in case.aPath:
            #print("DP :",path.x,path.y,path.z,path.d)
            c=self.getCase(path.x,path.y,path.z,path.d)

            c.displayGrey(cv2, self.img)
        case.displayGrey(cv2, self.img)
        cv2.imshow('img', self.img)
        if (stop == False):
            key = cv2.waitKey(1)
        else:
            key = cv2.waitKey(0) & 0x0FF

    def printAll(self):
        mx=self.x_max+1
        my=self.y_max+1
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
        mx = self.x_max + 1
        my = self.y_max + 1
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
        for z in range(0,self.z_max):
            for d in range(0, self.d_max):
                self.cases[x][y][z][d] = Case17(debug,heatloss,x,y,z,d,self.nb_cases)

        self.nb_cases += 1

    def setTotalHeatLoss(self,x,y,z,d,totalHeatLoss):
        self.cases[x][y][z][d].totalHeatLoss = totalHeatLoss


    def limitXYZ(self,x,y,z):
        limit,x,y=Univers.limitXY(self,x,y)
        if (z >= self.z_max):
            z = self.z_max-1
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
                p.append(Path(new.x,new.y,new.z,new.d,th))
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
        return self.cases[x][y][z][d]


    def start(self,x,y,z,d,min_forward):
        self.aCases=[]
        self.zmin=min_forward

        # init algo : set the first case into working queue
        case=self.getCase(x,y,z,d)
        case.aPath.append(Path(x, y, z, d,0))
        self.setTotalHeatLoss(x, y, z, d, 0)
        self.aCases.append(case)


        while len(self.aCases):
            #working queue not empty => test the case with lowest total heatLoss
            new=self.getLowest()
            x,y,z,d=new.getForward()
            self.addWorkingCase(self.aCases,new,x,y,z,d,)
            if(new.z>self.zmin-1):
                x, y, z, d = new.getRight()
                self.addWorkingCase(self.aCases,new,x,y,z,d)
            if(new.z>self.zmin-1):
                x, y, z, d = new.getLeft()
                self.addWorkingCase(self.aCases,new,x,y,z,d)
            #display every turn
            #self.displayPath(new.x, new.y, new.z, new.d, False)
        xfinal=self.x_max-1
        yfinal=self.y_max-1
        min=10000000
        zf=0
        df=0
        for z in range (0,self.z_max):
            for d in range(0, self.d_max):
                th=self.getCase(xfinal, yfinal, z, d).totalHeatLoss
                if(min>th):
                    zf=z
                    df=d
                    min=th
        # display part 1 and 2
        #self.displayPath(xfinal,yfinal,zf,df,True)
        return min

class Case17(Case):
    def __init__(self, debug, heatloss, x, y, z,d,num):
        Case.__init__(self, debug, heatloss, x, y, num,cCaseWidth,cCaseHeight)
        self.heatloss=int(heatloss)
        self.totalHeatLoss=10000
        self.aPath = []
        self.z = z
        self.d = d

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
        x, y, d=Case.getForward(self,self.d)
        z=self.z+1
        return x,y,z,d

    def getBackward(self):
        x, y, d  = Case.getBackward(self, self.d)
        z = self.z + 1
        return x, y, z, d

    def getRight(self):
        x, y, d = Case.getRight(self, self.d)
        z = 0
        return x, y, z, d

    def getLeft(self):
        x, y, d = Case.getLeft(self, self.d)
        z = 0
        return x, y, z, d

coef=1
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
                        x_max, y_max,max_forward,cCaseMaxDir,
                        np.array([[[[0 for d in range(cCaseMaxDir)] for z in range(max_forward)] for y in range(y_max)] for x in range(x_max)], dtype=Case17),
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


def runpart(debug, part,min_forward,max_forward):
    univers = getData(filename, part, debug,max_forward)
    result=univers.start(0,0,0,cCaseSouth,min_forward)
    return result


if __name__ == '__main__':
    debug = eVisulvl
    filename = './17.txt'
    part = 1

    print(f"Part 1 : {runpart(debug,1, 0,3)}")
    print(f"Part 2 : {runpart(debug,2, 3,10)}")



