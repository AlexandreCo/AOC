import re
import sys
class Game :


    def __init__(self,debug,hand,bid,valDict,part):
        self.debug=debug
        self.score=0
        self.hand=hand
        self.bid=bid
        self.cards=[]
        self.cardsValue=[]
        self.handName = 'None'
        self.handValue = 0
        self.valDict=valDict
        self.part = part
        self.typeDict = {
            'None' : 0,
            'HighCard' : 1,
            'OnePair' : 2,
            'TwoPair': 3,
            'ThreeOf' :4,
            'FullHouse' :5,
            'FourOf': 6,
            'FiveOf' : 7
        }
        for i,c in enumerate(self.hand):
            self.cards.append(c)

            if c.isdigit():
                self.cardsValue.append(int(c))
            else:
                self.cardsValue.append(self.valDict[c])

        if(self.isFiveOf((self.part==2))):
            self.handName = 'FiveOf'
        else:
            if(self.isFourOf((self.part==2))):
                self.handName = 'FourOf'
            else:
                if(self.isFullHouse((self.part==2))):
                    self.handName = 'FullHouse'
                else:
                    if(self.isThreeOf((self.part==2))):
                        self.handName = 'ThreeOf'
                    else:
                        if (self.isTwoPair((self.part == 2))):
                            self.handName = 'TwoPair'
                        else:
                            if (self.isOnePair((self.part == 2))):
                                self.handName = 'OnePair'
                            else:
                                self.handName = 'HighCard'

        self.setHandValue()
        if(self.debug):
            print(f"{self.hand} ", end="")
            print(f"{self.bid} ", end="")
            print(f"{self.handName} {hex(self.handValue)}",end="")
            if(self.debug > 1):
                print(f" ({self.getMaxValueInHand()}) ",end="")
            print(f"")

        assert self.handValue!=0
        assert self.typeDict[self.handName] != 0

    def __lt__(self, other):
        return self.handValue < other.handValue
    def setHandValue(self):
        self.handValue=self.typeValue()+self.strongValue()
    def typeValue(self):
        tValue=self.typeDict[self.handName]*0x100000
        return tValue
    def strongValue(self):
        mult=0x10000;
        strongValue=0;
        for i in range (0,5):
            strongValue+=self.cardsValue[i]*mult
            mult/=0x10
        return int(strongValue)

    def isFiveOf(self,joke):
        ret=False
        nb,nbj = self.getMaxValueInHand()
        if(nb[0]>=5):
            ret=True
        if(joke):
            if(self.isFourOf(False) and  (nbj>0)):
                ret=True
            if(self.isThreeOf(False) and (nbj>1)):
                if(nbj!=3):
                    ret=True
                else:
                    if(self.isFullHouse(True)):
                        ret = True
            if(self.isTwoPair(False) and (nbj>2)):
                ret=True
        return ret

    def isFourOf(self,joke):
        ret = False
        nb,nbj =  self.getMaxValueInHand()
        if (nb[0] == 4):
            ret = True
        if(joke):
            if(self.isThreeOf(False) and (nbj>0)):
                ret=True
            if(self.isTwoPair(False) and (nbj>1)):
                ret=True
        return ret

    def isFullHouse(self,joke):
        ret = False
        nb,nbj = self.getMaxValueInHand()
        if (nb[0] == 3):
            if (nb[1] == 2):
                ret = True
        if(joke):
            if(self.isTwoPair(False) and (nbj>0)):
                ret=True
        return ret

    def isThreeOf(self,joke):
        ret = False
        nb,nbj = self.getMaxValueInHand()
        if (nb[0] == 3):
            ret = True
        if (joke):
            if (self.isOnePair(False) and (nbj > 0)):
                ret = True
        return ret

    def isTwoPair(self,joke):
        ret = False
        nb,nbj = self.getMaxValueInHand()
        if (nb[0] == 2):
            if (nb[1] == 2):
                ret = True
        if (joke):
            if (self.isOnePair(False) and (nbj > 0)):
                ret = True
        return ret

    def isOnePair(self,joke):
        ret = False
        nb,nbj = self.getMaxValueInHand()
        if (nb[0] == 2):
            if (nb[1] == 1):
                ret = True
        if (joke):
            if(nbj > 0):
                ret = True
        return ret



    def getMaxValueInHand(self):
        max=0
        card=0
        nbof=[]
        tab = []
        nbJ=0
        def incValue(value,max,card):
            tab[value] += 1
            if (tab[value] > max):
                max = tab[value]
                card = value
            return max,card

        for i in range(15):
            tab.append(0)
        for cardValue in self.cardsValue:
            tab[cardValue]+=1
            if(tab[cardValue]>max):
                max=tab[cardValue]
                card=cardValue

        for i in range(15):
            if(tab[i]):
                nbof.append(tab[i])
        nbof.sort(reverse=True)
        nbJ=tab[self.valDict['J']]
        return nbof,nbJ

def getData(filename,games,part,debug):
    valDict1 = {
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
    }

    valDict2 = {
        'T': 10,
        'J': 1,
        'Q': 12,
        'K': 13,
        'A': 14,
    }

    if(part==1):
        valDict=valDict1
    else:
        valDict = valDict2
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        hand,bid=line.strip().split(" ")
        games.append(Game(debug,hand,int(bid),valDict,part))


def run(debug):

    result=0
    games.sort()
    rank=0

    for game in games:
        rank+=1
        result+=rank*game.bid
        if(debug):
            print(rank,game.cards,game.bid)
        #print(f"{rank}; {game.hand}; {game.handName}; {game.handValue}; {game.bid};")
    return result



if __name__ == '__main__':
    debug = 0
    #filename='./7-single.txt'
    filename = './7.txt'

    part=1

    games = []
    getData(filename,games,part,debug)
    print(f"Part 1 : {run(debug)}")

    games = []
    part+=1
    getData(filename,games,part,debug)
    print(f"Part 2 : {run(debug)}")




