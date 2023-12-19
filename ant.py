from debug import *


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

    def limitxy(self,x,y):
        limit=False
        if(y>self.ymax):
            y=self.ymax
            limit = True
        if(x>self.xmax):
            x=self.xmax
            limit = True
        if(x<self.xmin):
            x=self.xmin
            limit = True
        if(y<self.ymin):
            y=self.ymin
            limit = True
        return x,y,limit

    def limit(self):
        self.x,self.y,self.sleep=self.limitxy(self.x,self.y)

    def test(self,dir,nb):
        if(dir=='s'):
            x=self.x
            y=self.y+nb

        if(dir=='n'):
            x=self.x
            y=self.y-nb

        if(dir=='e'):
            x=self.x+nb
            y=self.y

        if(dir=='w'):
            x=self.x-nb
            y=self.y

        x, y, limit = self.limitxy(x, y)
        return x, y, int(self.cases[x][y].name),limit

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


    def display(self,cv2,img,cCaseWidth,cCaseHeight):
        dx = self.x * cCaseWidth
        dy = self.y * cCaseHeight
        if isDebug(self.debug, eDbglvl):
            print(f"ant : {self.x} {self.y}, {dx} {dy}")
        cv2.circle(img, (dx+int(cCaseWidth/2), dy+int(cCaseHeight/2)), int(cCaseHeight/5), (0, 0, 255), -1)
