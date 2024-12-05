import numpy as np

class Univers:

    def __init__(self, debug, x_max, y_max,cases):

        self.cases = cases
        self.debug = debug
        self.nb_cases = 0
        self.x_max = x_max
        self.y_max = y_max

        self.ants = []


    def getSize(self):
        if isDebug(debug, eDbglvl):
            print(f"univers size : {self.x_max} {self.y_max}")
        return self.x_max, self.y_max

    def countVisited(self, debug):
        ret = 0
        for y in range(0, self.y_max):
            for x in range(0, self.x_max):
                if(self.cases[x][y].count):
                    ret+=1
                if isDebug(debug, eDbglvl):
                    print(f" {ret}",end="")
            if isDebug(debug, eDbglvl):
                print("")
        return ret
    def getCase(self,x,y):
        return self.aCase[x][y];


    def limitXY(self,x,y):
        limit=False;
        if(x>=self.x_max):
            x=self.x_max-1
            limit=True
        if (y >= self.y_max):
            y = self.y_max-1
            limit = True
        if (x < 0 ):
            x = 0
            limit = True
        if (y < 0 ):
            y = 0
            limit = True
        return limit,x,y


