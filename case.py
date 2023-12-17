
class Case:
    def __init__(self, debug, name, x, y, num):
        self.debug = debug
        self.name = name
        self.x = x
        self.y = y


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