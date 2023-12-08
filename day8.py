import re
import sys

eNonelvl=0
eWarnlvl=1
eNoticelvl=2
eInfolvl=3
eDbglvl=4

class Ways :
    
    def __init__(self,debug,name,left,right):
        self.debug=debug
        self.name=name
        self.rightName=right
        self.leftName = left
        if (isDebug(debug, eDbglvl)):
            print(f"Ways {self.name} : New Ways L={self.leftName} R={self.rightName}")

    def __lt__(self, other):
        return 1

    def walk(self,direction):
        if(direction=='R'):
            return self.right
        else:
            if (direction == 'L'):
                return self.left
        assert(direction)

    def connect(self, left,right):
        self.right=right
        self.left = left



def isDebug(debug,lvl):
    if(debug>=lvl):
        return True
    else:
        return False
def getData(filename,network,map,part,debug):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    for i, c in enumerate(lines.pop(0).strip()):
        map.append(c)

    if (isDebug(debug,eInfolvl)):
        print(f"getData M={map}")

    lines.pop(0)
    for line in lines:
        name=line.split('=')[0].strip()
        left,right=line.split('=')[1].strip().replace('(','').replace(')','').split(",")
        left.strip()
        right.strip()
        if (isDebug(debug,eDbglvl)):
            print(f"getData : N={name} L={left} R={right}")
        network[name]=Ways(debug,name,left.strip(),right.strip())

    for name,ways in network.items():
        ways.connect(network[ways.leftName],network[ways.rightName])


def run(debug):
    result=0
    steps=0
    ways=network["AAA"]
    if (isDebug(debug, eDbglvl)):
        print(f"run : first {ways.name} L={ways.leftName} R={ways.rightName}")
    while True:
        for next in map:
            steps+=1
            ways=ways.walk(next)
            if (isDebug(debug, eInfolvl)):
                print(f"{steps} {next} {ways.name} ")
            if(ways.name=="ZZZ"):
                if (isDebug(debug, eInfolvl)):
                    print(f"End {steps}")
                result=steps
                return result
    assert (result)
    return result


if __name__ == '__main__':
    debug = eNonelvl
    #debug = eInfolvl
    filename = './8.txt'
    part=1
    network = {}
    map = []
    getData(filename,network,map,part,debug)
    print(f"Part 1 : {run(debug)}")


    network = {}
    map = []
    part+=1
    getData(filename,network,map,part,debug)
    print(f"Part 2 : {run(debug)}")




