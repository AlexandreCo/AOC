import re
import sys
import cv2
import numpy as np
from ant import *
from case import *
from debug import *
from univers import *

class Ant17(Ant):
    def __init__(self, debug, x, y,xmax,ymax,dir,cases):
        Ant.__init__(self, debug, x, y,xmax,ymax,dir,cases)



    def walk(self):
        if (self.sleep == True):
            return False, 'x'
        c1=self.test(self.dir,1)
        c2=self.test(self.dir,2)
        c3=self.test(self.dir,3)
        print(c1,c2,c3)
        return False, 'x'


class Univers17(Univers):

    def __init__(self, debug, init_x_max, init_y_max,cases ):
        Univers.__init__(self,debug,init_x_max, init_y_max ,cases )
        self.img = np.zeros((self.init_x_max*cCaseHeight, self.init_y_max*cCaseWidth, 3), np.uint8)
        cv2.namedWindow('visu')

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
            print(f"")

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

    def start(self,x,y,dir):
        a=Ant17(self.debug,x, y, self.init_x_max-1, self.init_y_max-1, dir, self.cases)
        self.ants.append(a)

        nb_worker = -1
        while nb_worker!=0:
            nb_worker=0
            for ant in self.ants:
                split,a = ant.walk()
                if(split):
                    self.ants.append(a)
                if(ant.sleep==False):
                    nb_worker+=1
            if(debug>eNonelvl):
                #self.display(eDbglvl,False,cCaseWidth, cCaseHeight,False)
                self.print()

class Case17(Case):
    def __init__(self, debug, name, x, y, num):
        Case.__init__(self, debug, name, x, y, num)

    def display(self, cv2, img, cCaseWidth, cCaseHeight):
        dx = self.x * cCaseWidth
        dy = self.y * cCaseHeight

        if (self.count):
            cv2.rectangle(img, (dx, dy), (dx + cCaseWidth, dy + cCaseHeight), (0x69, 0x69, 0x69), -1)
        if (self.name == '/'):
            cv2.line(img, (dx, dy + cCaseHeight), (dx + cCaseWidth, dy), (0, 255, 0), 1)
        if (self.name == '\\'):
            cv2.line(img, (dx, dy), (dx + cCaseWidth, dy + cCaseHeight), (0, 255, 0), 1)
        if (self.name == '|'):
            cv2.rectangle(img, (dx + int(cCaseWidth / 2) - 2, dy),
                          (dx + int(cCaseWidth / 2) + 2, dy + cCaseHeight), (0, 255, 0), 1)
        if (self.name == '-'):
            cv2.rectangle(img, (dx, dy + int(cCaseHeight / 2) - 2),
                          (dx + cCaseWidth, dy + int(cCaseHeight / 2) + 2), (0, 255, 0), 1)
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
    y_max = 0
    for line in lines:
        x_max = len(line)
        y_max += 1


    univers = Univers17(debug, x_max, y_max,np.array([[0 for x in range(y_max + 1)] for y in range(x_max + 1)], dtype=Case17))

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
    print(f"Part 2 : {runpart(debug,2)}")



