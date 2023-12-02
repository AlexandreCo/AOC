import re
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

Color = Enum('Color', ['RED', 'GREEN', 'BLUE'])
def spelledToNumber(line):
    line = line.replace(str("one"), "o1")
    line = line.replace(str("two"), "t2")
    line = line.replace(str("three"), "t3")
    line = line.replace(str("four"), "f4")
    line = line.replace(str("five"), "f5")
    line = line.replace(str("six"), "s6")
    line = line.replace(str("seven"), "s7")
    line = line.replace(str("eight"), "e8")
    line = line.replace(str("nine"), "n9")
    return line

def spelledToNumberRevers(line):
    line = line.replace(str("one")[::-1], "e1")
    line = line.replace(str("two")[::-1], "o2")
    line = line.replace(str("three")[::-1], "e3")
    line = line.replace(str("four")[::-1], "r4")
    line = line.replace(str("five")[::-1], "e5")
    line = line.replace(str("six")[::-1], "x6")
    line = line.replace(str("seven")[::-1], "n7")
    line = line.replace(str("eight")[::-1], "t8")
    line = line.replace(str("nine")[::-1], "e9")
    return line


def removeLetter(line) :
    return re.sub("[a-z]", "", line)


class cube:
    max=0
    nbCube=0
    max_bag=0
    def __init__(self, max_bag):
        self.max_bag=max_bag
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


if __name__ == '__main__':

    file = open('./2.txt', "r")
    lines = file.readlines()
    file.close()
    sum = 0
    nbline = 0
    #only 12 red cubes, 13 green cubes, and 14 blue cubes

    blue=cube(14)
    red=cube(12)
    green=cube(13)
    for line in lines:
        nbline += 1
        line=line.strip()
        blue.reset()
        red.reset()
        green.reset()
        print("line", line)
        sublines=line.split(":")
        for subline in sublines :
            #print(subline)
            subsets=subline.split(";")
            for subset in subsets:
                draws = subset.split(",")
                nbBlue = 0
                nbRed = 0
                nbGreen = 0
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
        print(blue.getMax(),red.getMax(),green.getMax())
        print(blue.valid(),red.valid(),green.valid())
        power=blue.getMax()*red.getMax()*green.getMax();
        print(power)
        sum+=power



    print(sum)
