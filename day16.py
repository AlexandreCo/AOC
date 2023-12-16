import re
import sys
import numpy as np

from day10 import eNonelvl

eNonelvl = 0
eWarnlvl = 1
eNoticelvl = 2
eInfolvl = 3
eDbglvl = 4

cGalaxy = '#'
cOther = '.'


class Case:
    def __init__(self, debug, name, x, y, num):
        self.debug = debug
        self.name = name
        self.x = x
        self.y = y
        self.num = 0

        self.aN=False
        self.aS = False
        self.aE = False
        self.aW = False
        if (name == cGalaxy):
            self.num = num

        if (isDebug(debug, eDbglvl)):
            if (self.name == cGalaxy):
                print(f"Case {num} : {x},{y}")

    def __lt__(self, other):
        return 1

    def display(self):
        if (self.name == cGalaxy):
            return self.num
        return self.name

    def visited(self,dir):
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
        self.xmax=xmax-1
        self.ymax=ymax-1
        self.xmin=0
        self.ymin=0
        self.dir=dir
        self.cases=cases
        print(f"ant : {x} {y}")

    def limit(self):
        if(self.y>self.ymax):
            self.y=self.ymax
        if(self.x>self.xmax):
            self.x=self.xmax
        if(self.x<self.xmin):
            self.x=self.xmin
        if(self.y<self.ymin):
            self.y=self.ymin


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
        if(dir=='s'):
            return 'e'
        if(dir=='e'):
            return 'n'
        if(dir=='w'):
            return 's'

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
            self.y -= 1
            self.limit()
        return self.getRight(dir)
    def getRight(self,dir):
        if(dir=='n'):
            return 'e'
        if(dir=='s'):
            return 'w'
        if(dir=='e'):
            return 's'
        if(dir=='w'):
            return 'n'
    def walk(self):
        dir=self.dir
        c=self.cases[self.x][self.y]
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
            self.dir=self.goRight(dir)
            a=Ant(debug,self.x,self.y,self.xmax,self.ymax,dir,self.cases)
            a.dir=a.goLeft(dir)
            return True,a

        return False, 'x'




class Univers:

    def __init__(self, debug, init_x_max, init_y_max):

        self.cases = np.array([[0 for x in range(init_y_max)] for y in range(init_x_max)], dtype=Case)
        self.debug = debug
        self.nb_cases = 0
        self.init_x_max = init_x_max
        self.init_y_max = init_y_max

        self.ants = []

    def addCase(self, name, x, y):
        debug = self.debug
        self.cases[x][y] = Case(debug,name,x,y,self.nb_cases)
        self.nb_cases += 1

    def getSize(self):
        if isDebug(debug, eDbglvl):
            print(f"univers size : {self.x_max} {self.y_max}")
        return self.x_max, self.y_max

    def display(self, debug):
        for y in range(0, self.init_y_max):
            for x in range(0, self.init_x_max):
                if(self.isAnt(x,y)):
                    if (debug >= eInfolvl):
                        print('x', end="")
                else:
                    if (debug >= eInfolvl):
                        S = self.cases[x][y].name
                        print(f"{S}", end="")
            if (debug >= eInfolvl):
                print(f"")

    def getCase(self,x,y):
        return self.aCase[x][y];

    def isAnt(self,x,y):
        for ant in self.ants:
            if(ant.x==x):
                if(ant.y==y):
                    return True
        return False

    def start(self,x,y,dir):

        a=Ant(self.debug,x, y, self.init_x_max, self.init_y_max, dir, self.cases)
        self.ants.append(a)

        while True:
            for ant in self.ants:
                split,a = ant.walk()
                if(split):
                    self.ants.append(a)
            self.display(eDbglvl)
            print("")












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
        x_max = len(line) - 1
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
    return result


def display(debug):
    univers.display(debug)


if __name__ == '__main__':
    debug = eNonelvl
    filename = './16-tiny.txt'
    part = 1
    univers = getData(filename, part, debug)
    univers.display(debug)
    display(debug)
    print(f"Part 1 : {runpart(debug, part, univers)}")
    # print(f"Part 2 : {runpart(debug,part,univers)}")



