import re
import sys
import numpy as np

eNonelvl = 0
eWarnlvl = 1
eNoticelvl = 2
eInfolvl = 3
eDbglvl = 4

cGalaxy = '#'
cOther = '.'
class Galaxie:
    def __init__(self, debug, name,x,y,num):
        self.debug = debug
        self.name = name
        self.x=x
        self.y=y
        self.num=0
        if(name==cGalaxy):
            self.num=num

        if (isDebug(debug, eDbglvl)):
            if(self.name==cGalaxy):
                print(f"Galaxie {num} : {x},{y}")

    def __lt__(self, other):
        return 1

    def isGalaxy(self):
        if(self.name==cGalaxy):
            return True
        else:
            return False
    def display(self):
        if(self.name==cGalaxy):
            return self.num
        return self.name


class Univers:

    def __init__(self, debug,init_x_max, init_y_max):

        self.symbol = np.array([[0 for x in range(init_y_max)] for y in range(init_x_max)])
        self.debug = debug
        self.nb_galaxies=0
        self.init_x_max = init_x_max
        self.init_y_max = init_y_max

        self.x_expand_max = init_x_max
        self.y_expand_max = init_y_max

        self.nbPairs=0
        self.gtab = []
    def addSymbol(self,name,x,y):
        debug=self.debug
        #debug=eDbglvl
        if (name == cGalaxy):
            self.nb_galaxies += 1
            self.symbol[x][y]=self.nb_galaxies
        else:
            self.symbol[x][y] = 0

    def addGalaxy(self,name,x,y):
        debug=self.debug
        if (debug >= eDbglvl):
            print(f"add {name} ({x},{y})")
        if (name!=0):
            self.nb_galaxies += 1
            self.agalaxy[x][y]=Galaxie(debug, cGalaxy,x,y,self.nb_galaxies)
            self.gtab.append(self.agalaxy[x][y])
        else:
            self.agalaxy[x][y]=Galaxie(debug, cOther,x,y,self.nb_galaxies)

    def expance(self,debug):
        nbExpance=0;
        tab=self.symbol.copy()
        for y in range(0, self.init_y_max):
            nbG=0;
            for x in range(0, self.init_x_max):
                S = tab[x][y]
                if (debug >= eDbglvl):
                    print(f"{S}", end="")
                if (S!=0):
                    nbG+=1
            if (debug >= eDbglvl):
                print(f"=> {nbG}", end="")

            if(nbG==0):
                if (debug >= eDbglvl):
                    print(f" expance {y}")
                self.symbol=np.insert(self.symbol,y+nbExpance,0,axis=1)
                self.y_expand_max+=1
                nbExpance+=1
            else:
                if (debug >= eDbglvl):
                    print(f"")

        nbExpance=0;
        for x in range(0, self.init_x_max):
            nbG=0;
            for y in range(0, self.init_y_max):
                S = tab[x][y]
                if (debug >= eDbglvl):
                    print(f"{S}", end="")
                if (S!=0):
                    nbG+=1
            if (debug >= eDbglvl):
                print(f"=> {nbG}", end="")

            if(nbG==0):
                if (debug >= eDbglvl):
                    print(f" expance {x}")
                self.symbol=np.insert(self.symbol,x+nbExpance,0,axis=0)
                self.x_expand_max+=1
                nbExpance+=1
            else:
                if (debug >= eDbglvl):
                    print(f"")
        self.nb_galaxies=0
        self.agalaxy    = np.array([[0 for x in range(self.y_expand_max)] for y in range(self.x_expand_max)], dtype=Galaxie)
        for y in range(0, self.y_expand_max):
            for x in range(0, self.x_expand_max):
                self.addGalaxy(self.symbol[x][y],x,y)




    def getSize(self):
        if isDebug(debug, eDbglvl):
            print(f"univers size : {self.x_max} {self.y_max}")
        return self.x_max,self.y_max


    def display(self,debug):
        for y in range(0, self.y_expand_max):
            for x in range(0, self.x_expand_max):
                S = self.agalaxy[x][y].display()
                if (debug >= eInfolvl):
                    print(f"{S}", end="")
            if (debug >= eInfolvl):
                print(f"")
    def displaySymbol(self,debug):
        for y in range(0, self.y_expand_max):
            for x in range(0, self.x_expand_max):
                S = self.symbol[x][y]
                if (debug >= eInfolvl):
                    if(S==0):
                        print(f".", end="")
                    else:
                        print(f"{S}", end="")
            if (debug >= eInfolvl):
                print(f"")

    def getGalaxy(self,idx):
        return self.gtab[idx-1]


    def getAllPairsOfGalaxies(self):
        self.pairs1 = []
        self.pairs2 = []
        self.nbPairs=0
        for galaxy1 in range(1,self.nb_galaxies+1):
            for galaxy2 in range(galaxy1+1, self.nb_galaxies+1):
                self.pairs1.append(galaxy1)
                self.pairs2.append(galaxy2)
                self.nbPairs+=1

        return self.nbPairs

    def getPairsOfGalaxies(self,idx):

        num1 = self.pairs1[idx]
        num2 = self.pairs2[idx]
        g1=self.getGalaxy(num1)
        g2=self.getGalaxy(num2)
        return g1,g2

    def getDistance(self,idx):
        g1,g2=self.getPairsOfGalaxies(idx)
        D=abs(g2.x-g1.x)+abs(g2.y-g1.y)
        if (self.debug >= eDbglvl):
            print(f"[{g1.num},{g2.num}] = {D}")
        return D

        

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
    y_max=0
    for line in lines:
        x_max=len(line)-1
        y_max+=1

    univers = Univers(debug,x_max,y_max)

    y=0
    for line in lines:
        x = 0

        for x, c in enumerate(line.strip()):

            if isDebug(debug,eDbglvl):
                print(f"[{x},{y} : {c} ]", end="")
            univers.addSymbol(c,x,y)

        if isDebug(debug,eDbglvl):
            print(f"")
        y += 1
    univers.expance(eInfolvl)
    return univers


def runpart(debug,part,univers):
    result = 0

    for i in range(0,univers.nb_galaxies):
        g1=univers.getGalaxy(i)

    nb_pairs=univers.getAllPairsOfGalaxies()
    for idx in range (0,nb_pairs):
        result+=univers.getDistance(idx)

    return result

def display(debug):
    univers.display(debug)

if __name__ == '__main__':
    debug = eNonelvl
    filename = './11.txt'
    part = 1
    univers=getData(filename, part, debug)
    display(debug)
    print(f"Part 1 : {runpart(debug,part,univers)}")
    #print(f"Part 2 : {runpart(debug,part,univers)}")



