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
    def __init__(self,x,y,heatloss,dir):
        self.x=x
        self.y=y
        self.heatloss=heatloss
        self.dir=dir

class Univers17(Univers):

    def __init__(self, debug, init_x_max, init_y_max,cases,cCaseWidth,cCaseHeight):
        Univers.__init__(self,debug,init_x_max, init_y_max ,cases )
        self.casesNS = cases.copy()
        self.casesEW = cases.copy()
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
                self.casesNS[x][y].display(cv2,self.img)
        cv2.imshow('img', self.img)
        if (stop == False):
            key = cv2.waitKey(1)
        else:
            key = cv2.waitKey(0) & 0x0FF

    def displayPath(self,x,y,stop,dir):
        self.displayU(False)
        case=self.getCase(x,y,dir)
        for path in case.aPath:
            c=self.getCase(path.x,path.y,dir)
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
        self.casesNS[x][y] = Case17(debug,heatloss,x,y,self.nb_cases)
        self.casesNS[x][y].nativedir=cCaseNorth
        self.casesEW[x][y] = Case17(debug, heatloss, x, y, self.nb_cases)
        self.casesEW[x][y].nativedir=cCaseEast

        self.nb_cases += 1

    def setTotalHeatLoss(self,x,y,totalHeatLoss,dir):
        self.casesNS[x][y].totalHeatLoss = totalHeatLoss
        self.casesEW[x][y].totalHeatLoss = totalHeatLoss
        # if(dir==cCaseNorth):
        #     self.casesNS[x][y].totalHeatLoss=totalHeatLoss
        # if (dir == cCaseSouth):
        #         self.casesNS[x][y].totalHeatLoss = totalHeatLoss
        # if(dir==cCaseEast):
        #     self.casesEW[x][y].totalHeatLoss=totalHeatLoss
        # if (dir == cCaseWest):
        #     self.casesEW[x][y].totalHeatLoss = totalHeatLoss
    def addWorkingCase(self,aCases,new, x, y,dir,max_count):


        size = len(new.aPath)
        #for i in range(0, size):
        #    print(new.aPath[-i].dir, end="")
        #print("")
        ret=True
        if (size >= max_count):
            #print(f"{dir}: ", end="")
            for i in range(1, max_count + 1):
                d=new.aPath[-i].dir
                #print(d, end="")
                if (d != dir):
                    ret=False
            #print(f"")
            #print(f"{i} {dir}")
            if (ret):
                #print("no way")
                return

        limit, x, y = self.limitXY(x, y)
        if (limit == False):
            neighbor=self.getCase(x,y,dir)
            h = new.totalHeatLoss + neighbor.heatloss
            th = neighbor.totalHeatLoss

            if (th > h):
                #neighbor.dir = dir
                th = h
                p = new.aPath.copy()
                p.append(Path(new.x,new.y,th,dir))
                neighbor.aPath = p
                self.setTotalHeatLoss(neighbor.x,neighbor.y,th,neighbor.nativedir)
                aCases.append(neighbor)

                # print(" : {0} {1} ".format(new.nativedir,
                #                                     chr(97+new.num))
                #                                     ,end="")
                # print(" : {0} {1}({2}) [".format(neighbor.nativedir, chr(97+neighbor.num),neighbor.totalHeatLoss)
                #
                #                                     ,end="")
                # for p in neighbor.aPath:
                #     print(p.dir,end="")
                # print("")

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


    def getCase(self,x,y,dir):
        if (dir==cCaseNorth):
            return self.casesNS[x][y]
        if (dir==cCaseSouth):
            return self.casesNS[x][y]
        if (dir == cCaseEast):
            return self.casesEW[x][y]
        if (dir == cCaseWest):
            return self.casesEW[x][y]

    def start(self,x,y,dir,max_count):
        self.aCases=[]

        x=1
        y=0
        case=self.getCase(x,y,dir)
        case.aPath.append(Path(0, 0, 0, cCaseEast))

        self.setTotalHeatLoss(x, y, case.heatloss,cCaseEast)
        #case.dir=dir
        self.aCases.append(case)

        while len(self.aCases):
            new=self.getLowest()
            #print(f"Get {new.x},{new.y}: {new.totalHeatLoss}")
            x,y=new.getNorth()
            self.addWorkingCase(self.aCases,new,x,y,cCaseNorth,max_count)
            x,y=new.getWest()
            self.addWorkingCase(self.aCases,new,x,y,cCaseWest,max_count)
            x,y=new.getEast()
            self.addWorkingCase(self.aCases,new,x,y,cCaseEast,max_count)
            x,y=new.getSouth()
            self.addWorkingCase(self.aCases,new,x,y,cCaseSouth,max_count)
            #self.printAll()
            #print("Queues:")
            #for case in self.aCases:
            #    print(f"{case.x},{case.y}: {case.totalHeatLoss}")
            #self.displayPath(new.x, new.y, True, new.nativedir)


        xfinal=self.init_x_max
        yfinal=self.init_y_max

        print("n:",self.getCase(xfinal, yfinal, cCaseNorth).totalHeatLoss)
        print("e:",self.getCase(xfinal, yfinal, cCaseEast).totalHeatLoss)
        self.displayPath(xfinal, yfinal, True, cCaseEast)
        self.displayPath(xfinal, yfinal, True, cCaseNorth)
        return 0
class Case17(Case):
    def __init__(self, debug, heatloss, x, y, num):
        Case.__init__(self, debug, heatloss, x, y, num,cCaseWidth,cCaseHeight)
        self.heatloss=int(heatloss)
        self.totalHeatLoss=10000
        self.aPath = []
        self.nativedir='x'

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
    result = 0
    univers = getData(filename, part, debug)
    #univers.printAllDir()
    #univers.displayU(True)
    result=univers.start(0,0,cCaseEast,3)
    return result


if __name__ == '__main__':
    debug = eVisulvl
    filename = './17.txt'
    part = 1

    print(f"Part 1 : {runpart(debug,1)}")
    #print(f"Part 2 : {runpart(debug,2)}")



