import re
import sys
import cv2
import numpy as np
from ant import *
from case import *
from debug import *


class Case16(Case):

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


coef=1
cCaseWidth=10*coef
cCaseHeight=8*coef

class Univers:


    def __init__(self, debug, init_x_max, init_y_max):

        self.cases = np.array([[0 for x in range(init_y_max+1)] for y in range(init_x_max+1)], dtype=Case)
        self.debug = debug
        self.nb_cases = 0
        self.init_x_max = init_x_max
        self.init_y_max = init_y_max

        self.ants = []

        self.img = np.zeros((self.init_x_max*cCaseHeight, self.init_y_max*cCaseWidth, 3), np.uint8)

        cv2.namedWindow('visu')


    def addCase(self, name, x, y):
        debug = self.debug
        self.cases[x][y] = Case16(debug,name,x,y,self.nb_cases)
        self.nb_cases += 1

    def getSize(self):
        if isDebug(debug, eDbglvl):
            print(f"univers size : {self.x_max} {self.y_max}")
        return self.x_max, self.y_max

    def display(self, debug,stop):
        if(isDebug(self.debug,eVisulvl)):
            self.img = np.zeros((self.init_x_max * cCaseHeight, self.init_y_max * cCaseWidth, 3), np.uint8)
            for y in range(0, self.init_y_max):
                for x in range(0, self.init_x_max):
                    self.cases[x][y].display(cv2,self.img,cCaseWidth,cCaseHeight)

            for ant in self.ants:
                ant.display(cv2,self.img,cCaseWidth,cCaseHeight)
            cv2.imshow('image originale', self.img)
            if(stop==False):
                key = cv2.waitKey(1)
            else:
                key = cv2.waitKey(0) & 0x0FF


    def countVisited(self, debug):
        ret = 0
        for y in range(0, self.init_y_max):
            for x in range(0, self.init_x_max):
                if(self.cases[x][y].count):
                    ret+=1
                if isDebug(debug, eDbglvl):
                    print(f" {ret}",end="")
            if isDebug(debug, eDbglvl):
                print("")
        return ret
    def getCase(self,x,y):
        return self.aCase[x][y];

    def isAnt(self,x,y):
        for ant in self.ants:
            if(ant.x==x):
                if(ant.y==y):
                    return True
        return False

    def start(self,x,y,dir):
        a=Ant(self.debug,x, y, self.init_x_max-1, self.init_y_max-1, dir, self.cases)
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
                self.display(eDbglvl,False)


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

    univers = Univers(debug, x_max, y_max)

    y = 0
    for line in lines:
        x = 0

        for x, c in enumerate(line.strip()):

            if isDebug(debug, eDbglvl):
                print(f"[{x},{y} : {c} ]", end="")
            univers.addCase(c, x, y)

        if isDebug(debug, eDbglvl):
            print(f"")
        y += 1

    return univers


def runpart(debug, part):
    result = 0
    for y in range(0,110):
        univers = getData(filename, part, debug)
        univers.start(0,y,'e')
        ret=univers.countVisited(debug)
        univers.display(debug, False)
        if(part==1):
            return ret

        if(ret>result):
            result=ret
        if(debug>=eDbglvl):
            print('ye',y,ret, result)

        univers = getData(filename, part, debug)
        univers.start(109, y, 'w')
        ret = univers.countVisited(debug)
        univers.display(debug, False)
        if (debug >= eDbglvl):
            print(ret)
        if (ret > result):
            result = ret
        if (debug >= eDbglvl):
            print('yw',y,ret, result)

    for x in range(0,110):
        univers = getData(filename, part, debug)
        univers.start(x,0,'s')
        ret=univers.countVisited(debug)
        univers.display(debug, False)
        if(part==1):
            return ret
        if (debug >= eDbglvl):
            print(ret)
        if(ret>result):
            result=ret
        if (debug >= eDbglvl):
            print('xs',x,ret, result)
        univers = getData(filename, part, debug)
        univers.start(x, 109, 'n')
        ret = univers.countVisited(debug)
        univers.display(debug, False)
        if (debug >= eDbglvl):
            print(ret)
        if (ret > result):
            result = ret
        if (debug >= eDbglvl):
            print('xn',x,ret, result)
    return result


def display(debug):
    if(debug>eNonelvl):
        univers.display(debug,False)


if __name__ == '__main__':
    debug = eVisulvl
    filename = './16.txt'
    part = 1

    print(f"Part 1 : {runpart(debug,1)}")
    print(f"Part 2 : {runpart(debug,2)}")



