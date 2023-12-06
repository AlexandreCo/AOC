import re

debug=0

class Race :

    def __init__(self,racetime,recordistance,id):
        self.racetime=racetime
        self.recordistance=recordistance
        self.debug=0
        self.id=id
        self.nbwin=0
        if(self.debug):
            print("new race ",self.id,self.racetime,self.recordistance)

    def win(self):
        self.nbwin+=1

def getData(filename,race):
    debug=0
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    line=lines.pop(0)
    ptimes=line.strip().split(":")[1].strip().replace("  "," ").replace("  "," ").replace("  "," ").split(" ")
    line=lines.pop(0)
    records=line.strip().split(":")[1].strip().replace("  "," ").replace("  "," ").replace("  "," ").split(" ")

    for  i in range(0,len(ptimes)):
        if(debug):
            print(ptimes[i],records[i])
        race.append(Race(int(ptimes[i]),int(records[i]),i))
    return i

def hold(remainingTime,ms):
    speed=ms
    remainingTime-=ms
    return remainingTime,speed

def test(remainingTime,speed):
    return remainingTime*speed

if __name__ == '__main__':
    debug = 0
    races = []

    result = 1
    getData('./6.txt',races)


    for race in races:
        for ms in range(0,race.racetime):
            remainingTime,speed=hold(race.racetime,ms)
            distance=test(remainingTime,speed)
            if(debug):
                print(race.racetime,ms,race.recordistance,distance,end="")
            if(distance>race.recordistance):
                race.win()
                if(debug):
                    print(" ok")
            else:
                if(debug):
                    print("")
        result*=race.nbwin


print(f"result : {result}")





