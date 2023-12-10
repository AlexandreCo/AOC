import re
import sys

eNonelvl = 0
eWarnlvl = 1
eNoticelvl = 2
eInfolvl = 3
eDbglvl = 4


class Pipe:

    def __init__(self, debug, name,x,y):
        self.debug = debug
        self.name = name
        self.x=x
        self.y=y
        if (isDebug(debug, eDbglvl)):
            print(f"Pipe {self.name}")

    def __lt__(self, other):
        return 1

    def connect(self, top, bottom):
        self.top = top
        self.bottom = bottom

    def east(self,x,y):
        if (self.name == 'J'):
            return self.x,self.y-1,'n'
        if (self.name == '-'):
            return self.x+1,self.y,'e'
        if (self.name == '7'):
            return self.x,self.y+1,'s'

    def north(self,x,y):
        if (self.name == '|'):
            return self.x,self.y-1,'n'
        if (self.name == '7'):
            return self.x-1,self.y,'w'
        if (self.name == 'F'):
            return self.x+1,self.y,'e'

    def south(self,x,y):
        if (self.name == '|'):
            return self.x,self.y+1,'s'
        if (self.name == 'J'):
            return self.x-1,self.y,'w'
        if (self.name == 'L'):
            return self.x+1,self.y,'e'

    def west(self,x,y):
        if (self.name == 'L'):
            return self.x,self.y-1,'n'
        if (self.name == '-'):
            return self.x-1,self.y,'w'
        if (self.name == 'F'):
            return self.x,self.y+1,'s'

    def walk(self,x,y,dir):
        if(dir=='e'):
            return self.east(x,y)
        if(dir=='n'):
            return self.north(x,y)
        if(dir=='s'):
            return self.south(x,y)
        if(dir=='w'):
            return self.west(x,y)
def isDebug(debug, lvl):
    if (debug >= lvl):
        return True
    else:
        return False


def getData(filename, part, debug):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    #
    j = 0
    max_raw=0
    for line in lines:
        max_col=len(line)-1
        max_raw+=1

    maze = [[0 for x in range(max_col)] for y in range(max_raw)]

    for line in lines:
        i = 0
        for i, c in enumerate(line.strip()):
            if isDebug(debug,eDbglvl):
                print(f"[{i},{j} : {c} ]", end="")
            maze[i][j]=Pipe(eNonelvl,c,i,j)
            if(c=='S'):
                door = i,j
        if isDebug(debug,eDbglvl):
            print(f"")
        j += 1

    return maze, door, max_col, max_raw

def isN(x,y):
    y-=1
    if(x>max_col):
        return False
    if(y>max_raw):
        return False
    if(x<0):
        return False
    if(y<0):
        return False

    name=maze[x][y].name
    if(name=='|'):
        return True
    if(name=='7'):
        return True
    if(name=='F'):
        return True
    return False

def isS(x,y):
    y+=1
    if(x>max_col):
        return False
    if(y>max_raw):
        return False
    if(x<0):
        return False
    if(y<0):
        return False

    name=maze[x,y].name
    if(name=='|'):
        return True
    if(name=='L'):
        return True
    if(name=='J'):
        return True
    return False

def isW(x,y):
    x-=1
    if(x>max_col):
        return False
    if(y>max_raw):
        return False
    if(x<0):
        return False
    if(y<0):
        return False

    name=maze[x,y].name
    if(name=='L'):
        return True
    if(name=='-'):
        return True
    if(name=='F'):
        return True
    return False


def isE(x,y):

    x+=1
    if(x>max_col):
        return False
    if(y>max_raw):
        return False
    if(x<0):
        return False
    if(y<0):
        return False

    name=maze[x][y].name

    if(name=='J'):
        return True
    if(name=='-'):
        return True
    if(name=='7'):
        return True
    return False

def run(debug,maze):
    result = 0

    x=door[0]
    y=door[1]

    if(isE(x,y)):
        x+=1
        dir = 'e'
    else:
        if (isN(x, y)):
            y-=1
            dir = 'n'
    step=1
    while True:
        step+=1
        next=maze[x][y].walk(x,y,dir)
        x = next[0]
        y = next[1]
        dir= next[2]
        if(maze[x][y].name=='S'):
            break


    return int(step/2)


if __name__ == '__main__':
    debug = eNonelvl
    # debug = eInfolvl
    filename = './10.txt'
    part = 1
    maze,door,max_col,max_raw=getData(filename, part, debug)
    print(f"Part 1 : {run(debug,maze)}")

    part += 1
    maze, door,max_col,max_raw=getData(filename, part, debug)
    print(f"Part 2 : {run(debug,maze)}")




