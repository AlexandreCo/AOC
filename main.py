import re
from enum import Enum
from array import *
#import numpy as nm

debug=0

estateSeed = -1
eStateSeedToSoil = estateSeed+1
eStateSoilToFertilizer = eStateSeedToSoil+1
eStateFertilizerToWater = eStateSoilToFertilizer+1
eStateWaterToLight = eStateFertilizerToWater+1
eStateLightToTemperature = eStateWaterToLight+1
eStateTemperatureToHumidity = eStateLightToTemperature+1
eStateHumidityToLocation = eStateTemperatureToHumidity+1
eMaxState=eStateHumidityToLocation+1

class ElemConverter :
    def __init__(self,type):
        self.type=type
        self.destRangeStartList = []
        self.srcRangeStartList=[]
        self.rangeLenghtList = []
        self.debug = 0

    def addElement(self,destRangeStart,srcRangeStart,rangeLenght):
        #print(f"{self.type} {destRangeStart}, {srcRangeStart}, {rangeLenght}")
        self.destRangeStartList.append(int(destRangeStart))
        self.srcRangeStartList.append(int(srcRangeStart))
        self.rangeLenghtList.append(int(rangeLenght))

    def displayElements(self):
        idx=0
        for destRangeStart in self.destRangeStartList:
            print(self.destRangeStartList[idx], self.srcRangeStartList[idx], self.rangeLenghtList[idx])
            idx+=1


    def convert(self,seed):
        debug=0
        idx=0
        result=seed
        for destRangeStart in self.destRangeStartList:
            start=self.srcRangeStartList[idx]
            end=self.srcRangeStartList[idx]+self.rangeLenghtList[idx]
            if(self.debug):
                print(f"[{start}-{end}],{seed}",end="")
            if(seed>=start):
                if (seed <= end):
                        result=seed+self.destRangeStartList[idx]-self.srcRangeStartList[idx]
                        if (self.debug):
                            print(f" ok : {result}")
                        return result
                else:
                    if (self.debug):
                        print(" ko")
            else:
                if (self.debug):
                    print(" ko")
            idx+=1

        if (self.debug):
            print(f" XX : {result}")
        return result

def testSeed(seed):
    tmp=int(seed)
    for i in range(eStateSeedToSoil,eMaxState):
        tmp=ElmtConvTab[i].convert(tmp)
    return tmp

if __name__ == '__main__':



    file = open('./5.txt', "r")
    lines = file.readlines()
    file.close()

    result = 0
    state = estateSeed
    ElmtConvTab=[0 for x in range(eMaxState)]

    seeds_list=lines.pop(0).split(":")[1].strip().split(" ")
    print(f"seedlist : {seeds_list}")


    for line in lines:
        if(len(line.strip())==0):
            #parse next section
            state+=1
            ElmtConvTab[state]=ElemConverter(state)
        else:
            element =line.strip().split(" ")
            if(len(element)==3):
                #real element
                ElmtConvTab[state].addElement(element[0],element[1],element[2])

    for seed in seeds_list:
        location=testSeed(seed)
        if(result==0):
            result=location
        else:
            if(location<result):
                result=location
    print(result)








