import numpy as np

class Univers:

    def __init__(self, debug, init_x_max, init_y_max,cases):

        self.cases = cases
        self.debug = debug
        self.nb_cases = 0
        self.init_x_max = init_x_max
        self.init_y_max = init_y_max

        self.ants = []


    def getSize(self):
        if isDebug(debug, eDbglvl):
            print(f"univers size : {self.x_max} {self.y_max}")
        return self.x_max, self.y_max


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



