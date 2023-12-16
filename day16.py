import re
import sys
import cv2
import numpy as np

from day10 import eNonelvl

eNonelvl = 0
eWarnlvl = 1
eNoticelvl = 2
eInfolvl = 3
eDbglvl = 4

coef=1
cCaseWidth=10*coef
cCaseHeight=8*coef

class Case:
    def __init__(self, debug, name, x, y, num):
        self.debug = debug
        self.name = name
        self.x = x
        self.y = y

        self.dx = x*cCaseWidth
        self.dy = y*cCaseHeight
        self.num = num

        self.aN = False
        self.aS = False
        self.aE = False
        self.aW = False

        self.count=0;

    def __lt__(self, other):
        return 1

    def isDirOk(self,dir):
        if(dir=='n'):
            return self.aN
        elif (dir=='s'):
            return self.aS
        elif (dir=='e'):
            return self.aE
        elif (dir=='w'):
            return self.aW
        return True
    def display(self,img):
        #if(self.name=='.'):
            #cv2.rectangle(img, (self.dx, self.dy), (self.dx + cCaseWidth, self.dy + cCaseHeight), (0, 255, 0), 1)
        if(self.count):
            cv2.rectangle(img, (self.dx, self.dy),  (self.dx + cCaseWidth, self.dy + cCaseHeight), (0x69, 0x69, 0x69), -1)
        if(self.name=='/'):
            cv2.line(img, (self.dx, self.dy + cCaseHeight), (self.dx + cCaseWidth, self.dy), (0, 255, 0), 1)
        if (self.name == '\\'):
            cv2.line(img,(self.dx, self.dy), (self.dx + cCaseWidth, self.dy + cCaseHeight),(0, 255, 0), 1)
        if (self.name == '|'):
            cv2.rectangle(img, (self.dx+int(cCaseWidth/2)-2, self.dy), (self.dx + int(cCaseWidth/2)+2, self.dy + cCaseHeight), (0, 255, 0), 1)
        if (self.name == '-'):
            cv2.rectangle(img, (self.dx, self.dy+int(cCaseHeight/2)-2), (self.dx+cCaseWidth , self.dy + int(cCaseHeight/2)+2), (0, 255, 0), 1)
        return self.name

    def visited(self,dir):
        self.count+=1
        if(dir=='n'):
            self.aN=True
        if(dir=='s'):
            self.aS=True
        if(dir=='e'):
            self.aE=True
        if(dir=='w'):
            self.aW=True
    def goForward(self,dir):
        self.visited(dir)
        if(self.name=='.'):
            return True

        if(self.name=='|'):
            if (dir == 'n'):
                return True
            if (dir == 's'):
                return True

        if(self.name=='-'):
            if (dir == 'w'):
                return True
            if (dir == 'e'):
                return True
        return False

    def goLeft(self,dir):
        self.visited(dir)
        if (self.name == '/'):
            if (dir == 'e'):
                return True
            if (dir == 'w'):
                return True
        if (self.name == '\\'):
            if (dir == 'n'):
                return True
            if (dir == 's'):
                return True
        return False

    def goRight(self,dir):
        self.visited(dir)
        if (self.name == '\\'):
            if (dir == 'e'):
                return True
            if (dir == 'w'):
                return True
        if(self.name == '/'):
            if (dir == 'n'):
                return True
            if (dir == 's'):
                return True

        return False
    def split(self,dir):
        self.visited(dir)
        if (self.name == '|'):
            if (dir == 'e'):
                return True
            if (dir == 'w'):
                return True
        if (self.name == '-'):
            if (dir == 'n'):
                return True
            if (dir == 's'):
                return True
        return False
class Ant:
    def __init__(self, debug, x, y,xmax,ymax,dir,cases):
        self.x=x
        self.y=y
        self.xmax=xmax
        self.ymax=ymax
        self.xmin=0
        self.ymin=0
        self.dir=dir
        self.cases=cases
        self.sleep=False
        self.debug=debug
        if isDebug(debug, eDbglvl):
            print(f"ant : {x} {y}")

    def limit(self):
        if(self.y>self.ymax):
            self.y=self.ymax
            self.sleep = True
        if(self.x>self.xmax):
            self.x=self.xmax
            self.sleep = True
        if(self.x<self.xmin):
            self.x=self.xmin
            self.sleep = True
        if(self.y<self.ymin):
            self.y=self.ymin
            self.sleep = True



    def goForward(self,dir):
        if(dir=='n'):
            self.y-=1
            self.limit()
        if(dir=='s'):
            self.y+=1
            self.limit()
        if(dir=='e'):
            self.x+=1
            self.limit()
        if(dir=='w'):
            self.x-=1
            self.limit()
        return self.getForward(dir)
    def getForward(self,dir):
        if(dir=='n'):
            return 'n'
        if(dir=='s'):
            return 's'
        if(dir=='e'):
            return 'e'
        if(dir=='w'):
            return 'w'
    def goLeft(self,dir):
        if(dir=='n'):
            self.x-=1
            self.limit()
        if(dir=='s'):
            self.x+=1
            self.limit()
        if(dir=='e'):
            self.y-=1
            self.limit()
        if(dir=='w'):
            self.y+=1
            self.limit()
        return self.getLeft(dir)

    def getLeft(self,dir):
        if(dir=='n'):
            return 'w'
        if(dir=='w'):
            return 's'
        if(dir=='s'):
            return 'e'
        if(dir=='e'):
            return 'n'

    def goRight(self,dir):
        if(dir=='n'):
            self.x+=1
            self.limit()
        if(dir=='s'):
            self.x-=1
            self.limit()
        if(dir=='e'):
            self.y+=1
            self.limit()
        if(dir=='w'):
            self.y-=1
            self.limit()
        return self.getRight(dir)
    def getRight(self,dir):
        if(dir=='n'):
            return 'e'
        if(dir=='e'):
            return 's'
        if(dir=='s'):
            return 'w'
        if(dir=='w'):
            return 'n'
    def walk(self):
        if(self.sleep==True):
            return False, 'x'

        dir=self.dir
        c=self.cases[self.x][self.y]

        if(c.isDirOk(dir)):
            self.sleep=True
            return False, 'x'

        if(c.goForward(dir)==True):
            self.dir=self.goForward(dir)
            return False, 'x'
        if (c.goLeft(dir) == True):
            self.dir=self.goLeft(dir)
            return False, 'x'
        if (c.goRight(dir) == True):
            self.dir=self.goRight(dir)
            return False, 'x'
        if(c.split(dir)):
            sister=Ant(self.debug,self.x,self.y,self.xmax,self.ymax,self.dir,self.cases)
            self.dir = self.getRight(dir)
            sister.dir=sister.getLeft(dir)
            return True,sister

        return False, 'x'


    def display(self,img):

        dx = self.x * cCaseWidth
        dy = self.y * cCaseHeight
        if isDebug(self.debug, eDbglvl):
            print(f"ant : {self.x} {self.y}, {dx} {dy}")
        cv2.circle(img, (dx+int(cCaseWidth/2), dy+int(cCaseHeight/2)), int(cCaseHeight/5), (0, 0, 255), -1)

class Univers:


    def __init__(self, debug, init_x_max, init_y_max):

        self.cases = np.array([[0 for x in range(init_y_max+1)] for y in range(init_x_max+1)], dtype=Case)
        self.debug = debug
        self.nb_cases = 0
        self.init_x_max = init_x_max
        self.init_y_max = init_y_max

        self.ants = []

        self.img = np.zeros((self.init_x_max*cCaseHeight, self.init_y_max*cCaseWidth, 3), np.uint8)

        cv2.namedWindow('image originale')


    def addCase(self, name, x, y):
        debug = self.debug
        self.cases[x][y] = Case(debug,name,x,y,self.nb_cases)
        self.nb_cases += 1

    def getSize(self):
        if isDebug(debug, eDbglvl):
            print(f"univers size : {self.x_max} {self.y_max}")
        return self.x_max, self.y_max

    def display(self, debug,stop):
        self.img = np.zeros((self.init_x_max * cCaseHeight, self.init_y_max * cCaseWidth, 3), np.uint8)
        for y in range(0, self.init_y_max):
            for x in range(0, self.init_x_max):
                self.cases[x][y].display(self.img)

        for ant in self.ants:
            ant.display(self.img)
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


def runpart(debug, part, univers):
    result = 0
    univers.start(0,0,'e')
    result=univers.countVisited(debug)
    univers.display(debug, True)
    return result


def display(debug):
    univers.display(debug,False)


if __name__ == '__main__':
    debug = eNonelvl
    filename = './16.txt'
    part = 1
    univers = getData(filename, part, debug)

    display(debug)

    print(f"Part 1 : {runpart(debug, part, univers)}")
    # print(f"Part 2 : {runpart(debug,part,univers)}")



