
class Case:
    def __init__(self, debug, name, x, y, num,cCaseWidth,cCaseHeight):
        self.debug = debug
        self.name = name
        self.x = x
        self.y = y
        self.cCaseWidth = cCaseWidth
        self.cCaseHeight = cCaseHeight

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

    def cv2DisplayXY(self, cv2, img, dx, dy, txt):
        font = cv2.FONT_HERSHEY_PLAIN
        org = (dx, dy)
        # fontScale
        fontScale = 1
        # Blue color in BGR
        color = (255, 0, 0)
        # Line thickness of 2 px
        thickness = 2
        image = cv2.putText(img, txt, org, font,
                            fontScale, color, thickness, cv2.LINE_AA)

    def cv2DisplayCenter(self, cv2, img, txt):
        w = self.cCaseWidth
        h = self.cCaseHeight
        dx = self.x * w + int(1 * w / 3)
        dy = self.y * h + int(2 * w / 3) - 2
        self.cv2DisplayXY(cv2, img, dx, dy, txt)

    def cv2DisplayNorth(self, cv2, img, txt):
        w = self.cCaseWidth
        h = self.cCaseHeight
        dx = self.x * w + int(1 * w / 3)
        dy = self.y * h + int(1 * w / 3) - 2
        self.cv2DisplayXY(cv2, img, dx, dy, txt)

    def cv2DisplaySouth(self, cv2, img, txt):
        w = self.cCaseWidth
        h = self.cCaseHeight
        dx = self.x * w + int(1 * w / 3)
        dy = self.y * h + int(3 * w / 3) - 2
        self.cv2DisplayXY(cv2, img, dx, dy, txt)

    def cv2DisplayEast(self, cv2, img, txt):
        w = self.cCaseWidth
        h = self.cCaseHeight
        dx = self.x * w + int(2 * w / 3)
        dy = self.y * h + int(2 * w / 3) - 2
        self.cv2DisplayXY(cv2, img, dx, dy, txt)

    def cv2DisplayWest(self, cv2, img, txt):
        w = self.cCaseWidth
        h = self.cCaseHeight
        dx = self.x * w + int(0 * w / 3)
        dy = self.y * h + int(2 * w / 3) - 2
        self.cv2DisplayXY(cv2, img, dx, dy, txt)
    def cv2DisplayBack(self,cv2,img,bgr):

        w=self.cCaseWidth
        h=self.cCaseHeight
        dx = self.x * w
        dy = self.y * h

        cv2.rectangle(img,
                      (dx, dy),
                      (dx + w, dy + h),
                      bgr, -1)

    def getEast(self):
        return self.x+1,self.y
    def getWest(self):
        return self.x-1,self.y
    def getNorth(self):
        return self.x,self.y-1
    def getSouth(self):
        return self.x,self.y+1