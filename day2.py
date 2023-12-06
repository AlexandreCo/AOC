import re
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

Color = Enum('Color', ['RED', 'GREEN', 'BLUE'])

class cube:

    def __init__(self, max_bag):
        self.max_bag=max_bag
        self.max=0
        self.nbCube=0

    def draw(self, newCubes):
        self.nbCube = self.nbCube + newCubes
        if( newCubes > self.max ):
            self.max = newCubes

    def getMax(self):
        return self.max;

    def getNumber(self):
        return self.nbCube

    def reset(self):
        self.max = 0
        self.nbCube = 0

    def valid(self):
        if(self.max > self.max_bag ):
            return False
        else:
            return True

def run(part):
    sum = 0
    nbline = 0
    blue=cube(14)
    red=cube(12)
    green=cube(13)
    for line in lines:
        nbline += 1
        line=line.strip()
        blue.reset()
        red.reset()
        green.reset()
        sublines=line.split(":")
        for subline in sublines :
            subsets=subline.split(";")
            for subset in subsets:
                draws = subset.split(",")
                for draw in draws:
                    objs=draw.split(" ")
                    if(objs[0] != "Game"):
                        nb=int(objs[1])
                        color=objs[2]
                        if color == "blue":
                            blue.draw(nb)
                        if color == "red":
                            red.draw(nb)
                        if color == "green":
                            green.draw(nb)
        if(part==2):
            power=blue.getMax()*red.getMax()*green.getMax();
            sum+=power
        if(part==1):
            if (blue.valid() & red.valid() & green.valid()):
                sum += nbline
    return sum
if __name__ == '__main__':

    file = open('./2.txt', "r")
    lines = file.readlines()
    file.close()
    print(f"Part 1 : {run(1)}")
    print(f"Part 2 : {run(2)}")
