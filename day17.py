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
    def __init__(self, x, y,dir,heatloss):
        self.x=x
        self.y=y
        self.dir=dir
        self.heatloss=heatloss

class Ant17(Ant):
    def __init__(self, debug, x, y,xmax,ymax,dir,cases,heatloss,aPath):
        Ant.__init__(self, debug, x, y,xmax,ymax,dir,cases)
        self.heatloss=heatloss
        self.aPath = aPath

    def min(self,c1,c2,c3):
        ret=0
        if(c1<c2):
            if (c1 < c3):
                ret = 1
            else:
                ret = 3
        else:
            if (c2 < c3):
                ret = 2
            else:
                ret = 3
        return ret


    def walk(self):
        p=Path(self.x, self.y, self.dir, self.heatloss)
        if (self.sleep == True):
            return False, 'x'
        if(self.cases[self.x][self.y].isDirOk(self.dir)==False):
            #Mark current as visited
            self.cases[self.x][self.y].visited(self.dir)
            if(self.x==self.xmax):
                if (self.y == self.ymax):
                    print('Path found',self.heatloss)
                    self.sleep=True
                    for i in range(0,len(self.aPath)):
                        print(self.aPath[i].x,self.aPath[i].y,self.aPath[i].dir,self.aPath[i].heatloss)
                    return False, 'x'
        else:
            self.sleep=True
            return False, 'x'

        #get case that minimize heat loss
        x,y,c1,limit =self.test(self.dir,1)
        if(limit):
            #no way
            self.sleep=True
            return False, 'x'
        else:
            x,y,c2,limit =self.test(self.dir,2)
            if(limit):
                #just one case before the limit
                step=1
                self.heatloss+=int(c1)
            else:
                x,y,c3,limit =self.test(self.dir,3)
                if(limit):
                    # just two case before limit (test 1 and 2)
                    step=self.min(c1,c2,1000)
                    if(step==1):
                        self.heatloss += int(c1)
                    else:
                        self.heatloss += int(c1)
                        self.heatloss += int(c2)
                else:
                    # a least three case limit (test 1, 2 and 3)
                    step = self.min(c1, c2, c3)
                    if(step==1):
                        self.heatloss += int(c1)
                    else:
                        if (step == 2):
                            self.heatloss += int(c1)
                            self.heatloss += int(c2)
                        else:
                            self.heatloss += int(c1)
                            self.heatloss += int(c2)
                            self.heatloss += int(c3)


            self.aPath.append(p)


        #Walk on this case
        self.x, self.y,name,limit=self.test(self.dir,step)

        #go left
        sister = Ant17(self.debug, self.x, self.y, self.xmax, self.ymax, self.dir, self.cases,self.heatloss,self.aPath)

        self.dir=self.getLeft(self.dir)
        sister.dir = sister.getRight(sister.dir)
        return True, sister



class Univers17(Univers):

    def __init__(self, debug, init_x_max, init_y_max,cases ):
        Univers.__init__(self,debug,init_x_max, init_y_max ,cases )
        self.img = np.zeros((self.init_x_max*cCaseHeight, self.init_y_max*cCaseWidth, 3), np.uint8)
        #cv2.namedWindow('visu')

    def display(self, cv2, img, cCaseWidth, cCaseHeight,stop):
        if (isDebug(self.debug, eVisulvl)):
            self.img = np.zeros((self.init_x_max * cCaseHeight, self.init_y_max * cCaseWidth, 3), np.uint8)
        for y in range(0, self.init_y_max):
            for x in range(0, self.init_x_max):
                if (isDebug(self.debug, eVisulvl)):
                    self.cases[x][y].display(cv2,self.img,cCaseWidth,cCaseHeight)
                else:
                    c=self.cases[x][y].name
                    print(f"{c: 2d}",end="")
            if (isDebug(self.debug, eVisulvl)==False):
                print(f"")

        for ant in self.ants:
            ant.display(cv2, self.img, cCaseWidth, cCaseHeight)
        cv2.imshow('img', self.img)
        if (stop == False):
            key = cv2.waitKey(1)
        else:
            key = cv2.waitKey(0) & 0x0FF
    def print(self):
        print(self.init_x_max,self.init_y_max)
        for y in range(0, self.init_y_max):
            for x in range(0, self.init_x_max):
                c=self.cases[x][y].getName()
                print(c,end="")
            print(f"")

    def addCase(self, name, x, y):
        debug = self.debug
        self.cases[x][y] = Case17(debug,name,x,y,self.nb_cases)
        self.nb_cases += 1

    def getLowest(self):
        heatloss = -1
        ret = False
        lowest=None
        for ant in self.ants:
            if(ant.sleep==False):
                hl=ant.heatloss
                if(heatloss==-1):
                    heatloss=hl
                    lowest=ant
                    ret=True
                else:
                    if(hl<heatloss):
                        heatloss = hl
                        lowest = ant
                        ret = True

        return ret,lowest
    def start(self,x,y,dir):
        a=Ant17(self.debug,x, y, self.init_x_max-1, self.init_y_max-1, dir, self.cases,0,[])
        self.ants.append(a)

        nb_worker = -1
        while True:
            nb_worker=0
            ret,ant=self.getLowest()
            if(ret==True):
                split,a = ant.walk()
                if(split):
                    self.ants.append(a)
                if(debug>eNonelvl):
                    #self.print()
                    self.display(cv2,self.img,cCaseWidth, cCaseHeight,False)
            else:
                break


class Case17(Case):
    def __init__(self, debug, name, x, y, num):
        Case.__init__(self, debug, name, x, y, num)

    def display(self, cv2, img, cCaseWidth, cCaseHeight):
        dx = self.x * cCaseWidth
        dy = self.y * cCaseHeight
        #print(self.x,self.y,dx,dy)

        #print(int(self.name)*25)
        cv2.rectangle(img, (dx, dy), (dx + cCaseWidth, dy + cCaseHeight), (int(self.name)*25, 0, 0), -1)

        return self.name

    def getName(self):
        return self.name

coef=1
cCaseWidth=10*coef
cCaseHeight=8*coef


def isDebug(debug, lvl):
    if (debug >= lvl):
        return True
    else:
        return False


def getData(filename, part, debug):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    j = 0
    y_max = 1
    for line in lines:
        x_max = len(line)
        y_max += 1


    univers = Univers17(debug, x_max-1, y_max-1,np.array([[0 for x in range(y_max + 1)] for y in range(x_max + 1)], dtype=Case17))

    y = 0
    for line in lines:
        x = 0
        for x, c in enumerate(line.strip()):
            if isDebug(debug, eDbglvl):
                print(f"[{x},{y} : {c} ]", end="")
            univers.addCase(c,x, y)

        if isDebug(debug, eDbglvl):
            print(f"")
        y += 1
    univers.print()
    return univers


def runpart(debug, part):
    result = 0
    univers = getData(filename, part, debug)

    univers.start(0,0,'e')
    return result


def display(debug):
    if(debug>eNonelvl):
        univers.display(debug,False)


if __name__ == '__main__':
    debug = eVisulvl
    filename = './17-tiny.txt'
    part = 1

    print(f"Part 1 : {runpart(debug,1)}")
    #print(f"Part 2 : {runpart(debug,2)}")



