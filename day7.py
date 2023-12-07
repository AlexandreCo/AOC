import re
import sys
debug=0

class Game :


    def __init__(self,debug,hand,bid,valDict):
        self.debug=debug
        self.score=0
        self.hand=hand
        self.bid=bid
        self.cards=[]
        self.cardsValue=[]
        self.handName = 'None'
        self.handValue = 0
        self.valDict=valDict

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


        if(self.isFiveOf()):
            self.handName = 'FiveOf'
        else:
            if(self.isFourOf()):
                self.handName = 'FourOf'
            else:
                if(self.isFullHouse()):
                    self.handName = 'FullHouse'
                else:
                    if(self.isThreeOf()):
                        self.handName = 'ThreeOf'
                    else:
                        if(self.isOnePair()):
                            self.handName = 'OnePair'
                        else:
                            if(self.isTwoPair()):
                                self.handName = 'TwoPair'

        self.setHandValue()
        if(self.debug):
            print(self.cards,self.cardsValue,self.bid,end='')
            print(f" {self.handName} {hex(self.handValue)}")

        assert self.handValue!=0

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

    def isFiveOf(self):
        ret=False
        nb, value = self.getMaxValueInHand()
        if(nb[0]==5):
            ret=True
        return ret

    def isFourOf(self):
        ret = False
        nb, value = self.getMaxValueInHand()
        if (nb[0] == 4):
            ret = True
        return ret

    def isFullHouse(self):
        ret = False
        nb, value = self.getMaxValueInHand()
        if (nb[0] == 3):
            if (nb[1] == 2):
                ret = True
        return ret

    def isThreeOf(self):
        ret = False
        nb, value = self.getMaxValueInHand()
        if (nb[0] == 3):
            if (nb[1] == 1):
                ret = True
        return ret

    def isTwoPair(self):
        ret = False
        nb, value = self.getMaxValueInHand()
        if (nb[0] == 2):
            if (nb[1] == 2):
                ret = True
        return ret

    def isOnePair(self):
        ret = False
        nb, value = self.getMaxValueInHand()
        if (nb[0] == 2):
            if (nb[1] == 1):
                ret = True
        return ret

    def getMaxValueInHand(self):
        max=0
        card=0
        nbof=[]
        tab = []
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
        return nbof,card

def getData(filename,games,part):
    ldebug=debug
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
        games.append(Game(ldebug,hand,int(bid),valDict))


def run(cards,part):
    ldebug = debug
    result=0
    games.sort()
    rank=0

    for game in games:
        rank+=1
        result+=rank*game.bid
        if(ldebug):
            print(rank,game.cards,game.bid)
    return result



if __name__ == '__main__':
    debug = 0
    filename='./7-tiny.txt'
    filename = './7.txt'
    games = []
    getData(filename,games,1)
    print(f"Part 1 : {run(games,1)}")

    games = []
    getData(filename,games,0)
    print(f"Part 2 : {run(games,2)}")




