import re
import sys




class Pipe:

    def __init__(self, debug, name,x,y):
        self.debug = debug
        self.dir='x'
        self.up =False
        self.dn = False
        self.name = name
        self.limit=False
        self.x=x
        self.y=y
        if (isDebug(debug, eDbglvl)):
            print(f"Pipe {self.name}")

    def name2shape(self,name):
        if(name=='-'):
            return '═'
        if(name=='|'):
            return '║'
        if(name=='F'):
            return '╔'
        if (name == '7'):
            return '╗'
        if (name == 'L'):
            return '╚'
        if (name == 'J'):
            return '╝'
        if (name == 'S'):
            return '#'
        if (name == 'I'):
            return '*'
        if (name == 'O'):
            return ' '
    def shape(self):
        if(self.limit==True):
            return self.name2shape(self.name)
        else:
            return self.name2shape(self.name)

    def gdir(self):
        if(self.limit==True):
            if(self.up):
                return "^"
            else:
                if (self.dn):
                    return "v"
                else:
                    return " "
        else:
            return " "
    def __lt__(self, other):
        return 1

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
        self.limit=True
        if(dir=='e'):
            nx,ny,ndir=self.east(x,y)

        if(dir=='n'):
            nx,ny,ndir=self.north(x,y)

        if(dir=='s'):
            nx,ny,ndir=self.south(x,y)

        if(dir=='w'):
            nx,ny,ndir=self.west(x,y)
        if(ndir=='s'):
            self.up=True
        if(dir=='n'):
            self.dn = True

        self.dir = ndir
        return nx,ny,ndir
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

    maze = [[0 for x in range(max_raw)] for y in range(max_col)]
    y=0
    for line in lines:
        x = 0
        for x, c in enumerate(line.strip()):
            if isDebug(debug,eDbglvl):
                print(f"[{x},{y} : {c} ]", end="")
            maze[x][y]=Pipe(eNonelvl,c,x,y)
            if(c=='S'):
                door = x,y
        if isDebug(debug,eDbglvl):
            print(f"")
        y += 1

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

    name=maze[x][y].name
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

    name=maze[x][y].name
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

def runpart1(debug,maze):
    result = 0

    x=door[0]
    y=door[1]
    maze[x][y].limit=True
    maze[x][y].name='S'
    maze[x][y].dir = 'n'
    maze[x][y].dn=True
    if(isE(x,y)):
        x+=1
        dir = 'e'
    else:
        if (isN(x, y)):
            y-=1
            dir = 'n'
        else:
            if (isS(x, y)):
                y += 1
                dir = 's'
            else:
                if (isW(x, y)):
                    x -= 1
                    dir = 'w'
                else:
                    assert True
                    assert False
    step=1
    print(x,y)
    while True:
        step+=1
        next=maze[x][y].walk(x,y,dir)
        #display(eInfolvl)
        x = next[0]
        y = next[1]
        dir= next[2]
        if(maze[x][y].name=='S'):
            break


    return int(step/2)

def runpart2(debug,maze):
    result=0
    for y in range(0, max_raw):
        inLoop = 0
        for x in range(0,max_col):
            if(maze[x][y].limit):
                if(maze[x][y].gdir()=='^'):
                    inLoop += 1
                else:
                    if (maze[x][y].gdir() == 'v'):
                        inLoop -= 1
            else:
                if(inLoop%2==1):
                    maze[x][y].name="I"
                    result+=1
                else:
                    maze[x][y].name = "O"
    return result

def display(debug):
    for y in range(0, max_raw):
        for x in range(0, max_col):
            S=maze[x][y].shape()
            D=maze[x][y].gdir()
            if(debug==eDbglvl):
                print(f"{S}{D}",end="")
            else:
                if (debug == eInfolvl):
                    print(f"{S}", end="")

        S = maze[x][y].shape()
        D = maze[x][y].gdir()
        if (debug == eDbglvl):
            print(f"{S}{D}")
        else:
            if (debug == eInfolvl):
                print(f"{S}")



if __name__ == '__main__':
    debug = eNonelvl
    filename = './10.txt'
    part = 1
    maze,door,max_col,max_raw=getData(filename, part, debug)
    print(f"Part 1 : {runpart1(debug,maze)}")
    print(f"Part 2 : {runpart2(debug,maze)}")
    display(debug)


