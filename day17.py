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
        self.id=0
        self.nbForward=0

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
            #ant sleeping
            return False, 'x','x'

        if(self.nbForward>3):
            self.sleep = True
            return False, 'x', 'x'

        #Mark current as visited
        #print("ant ",self.id," : ",end="")
        if(self.cases[self.x][self.y].visited(self.dir,self.heatloss)==False):
            #bigger Heatloss
            self.sleep = True
            return False, 'x','x'

        if(self.x==self.xmax):
            if (self.y == self.ymax):
                print("ant ",self.id," : Path found",self.heatloss)
                self.sleep=True
                # for i in range(0,len(self.aPath)):
                #     print(self.aPath[i].x,self.aPath[i].y,self.aPath[i].dir,self.aPath[i].heatloss)
                return False, 'x','x'

        #get case that minimize heat loss
        x,y,c1,limit =self.test(self.dir,1)
        if(limit):
            #no way
            self.sleep=True
            return False, 'x','x'
        else:
            # Walk on this case
            self.heatloss+=int(c1)
            self.nbForward+=1
            self.x, self.y, name, limit = self.test(self.dir, 1)
            self.aPath.append(p)

            #add sister at left
            sisterL = Ant17(self.debug, self.x, self.y, self.xmax, self.ymax, self.dir, self.cases,
                            self.heatloss, self.aPath)
            sisterL.dir = sisterL.getLeft(sisterL.dir)

            # add sister at right
            sisterR = Ant17(self.debug, self.x, self.y, self.xmax, self.ymax, self.dir, self.cases,
                            self.heatloss, self.aPath)
            sisterR.dir = sisterR.getRight(sisterR.dir)
            return True, sisterL,sisterR




    def display(self,cv2,img,cCaseWidth,cCaseHeight):
        dx = self.x * cCaseWidth
        dy = self.y * cCaseHeight
        if isDebug(self.debug, eDbglvl):
            print(f"ant : {self.x} {self.y}, {dx} {dy}")

        # font = cv2.FONT_HERSHEY_SIMPLEX
        # # org
        # org = (dx, dy+int(cCaseHeight))
        # # fontScale
        # fontScale = 1
        # # Blue color in BGR
        # color = (0, 0, 255)
        # # Line thickness of 2 px
        # thickness = 1
        # disp=str(self.heatloss)+" "+str(self.nbForward)
        # image = cv2.putText(img, disp, org, font,
        #                     fontScale, color, thickness, cv2.LINE_AA)

        cv2.circle(img, (dx+int(cCaseWidth/2), dy+int(cCaseHeight/2)), int(cCaseHeight/5), (0, 0, 255), -1)


class Univers17(Univers):

    def __init__(self, debug, init_x_max, init_y_max,cases ):
        Univers.__init__(self,debug,init_x_max, init_y_max ,cases )
        self.img = np.zeros((self.init_x_max*cCaseHeight, self.init_y_max*cCaseWidth, 3), np.uint8)
        self.stepByStep=False
        #cv2.namedWindow('visu')

    def displayU(self, cv2, img, cCaseWidth, cCaseHeight,stop):
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
        nbAnt=0
        idAnt=0
        for ant in self.ants:
            ant.id=idAnt
            idAnt+=1
            if(ant.sleep==False):
                nbAnt+=1
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
        #print("ants : ",nbAnt)
        return ret,lowest
    def start(self,x,y,dir):
        a=Ant17(self.debug,x, y, self.init_x_max-1, self.init_y_max-1, dir, self.cases,0,[])
        self.ants.append(a)

        nb_worker = -1
        while True:
            nb_worker=0
            ret,ant=self.getLowest()
            if(ret==True):
                split,l,r = ant.walk()
                if(split):
                    self.ants.append(l)
                    self.ants.append(r)
                if(debug>eNonelvl):
                    #self.print()
                    self.displayU(cv2,self.img,cCaseWidth, cCaseHeight,self.stepByStep)
            else:
                break


class Case17(Case):
    def __init__(self, debug, name, x, y, num):
        Case.__init__(self, debug, name, x, y, num)
        self.heatlossE=-1
        self.heatlossW=-1
        self.heatlossN=-1
        self.heatlossS=-1

    def display(self, cv2, img, cCaseWidth, cCaseHeight):
        dx = self.x * cCaseWidth
        dy = self.y * cCaseHeight
        #print(self.x,self.y,dx,dy)

        #print(int(self.name)*25)
        cv2.rectangle(img, (dx, dy), (dx + cCaseWidth, dy + cCaseHeight), (int(self.name)*25, 0, 0), -1)

        # font = cv2.FONT_HERSHEY_SIMPLEX
        # # org
        # org = (dx+int(cCaseWidth/2), dy+int(cCaseHeight/2))
        # # fontScale
        # fontScale = 1
        # # Blue color in BGR
        # color = (255, 0, 0)
        # # Line thickness of 2 px
        # thickness = 2
        # image = cv2.putText(img, str(self.name), org, font,
        #                     fontScale, color, thickness, cv2.LINE_AA)

        return self.name

    def getName(self):
        return self.name

    def visited(self, dir,heatloss):
        #print(self.x,self.y,heatloss,dir,self.heatlossN,self.heatlossS,self.heatlossE,self.heatlossW)
        if(dir=='n'):
            if(self.heatlossN==-1):
                self.heatlossN=heatloss
                return True
            else:
                if(self.heatlossN>heatloss):
                    self.heatlossN=heatloss
                    return True
        if(dir=='s'):
            if(self.heatlossS==-1):
                self.heatlossS=heatloss
                return True
            else:
                if(self.heatlossS>heatloss):
                    self.heatlossS=heatloss
                    return True
        if(dir=='e'):
            if(self.heatlossE==-1):
                self.heatlossE=heatloss
                return True
            else:
                if(self.heatlossE>heatloss):
                    self.heatlossE=heatloss
                    return True
        if(dir=='w'):
            if(self.heatlossW==-1):
                self.heatlossW=heatloss
                return True
            else:
                if(self.heatlossW>heatloss):
                    self.heatlossW=heatloss
                    return True

        return False


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



