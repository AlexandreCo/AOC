import re
from enum import Enum
from array import *
#import numpy as nm

debug=0

cSampleLength=1000000

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
        self.debug=0
        idx=0
        result=seed
        for destRangeStart in self.destRangeStartList:

            start=self.srcRangeStartList[idx]
            end=self.srcRangeStartList[idx]+self.rangeLenghtList[idx]
            if(seed>=start):
                if (seed < end):
                        result=seed+self.destRangeStartList[idx]-self.srcRangeStartList[idx]
                        if (self.debug):
                            print(f"{self.type}:[{start}-{end}],{seed}", end="")
                            print(f" ok : {result}")
                        return result
            idx+=1

        if (self.debug):
            print(f"{self.type}:[XX-XX] ,{seed}", end="")
            print(f" ok : {result}")
        return result

def testSeed(seed):
    debug=0
    tmp=int(seed)
    if(debug):
        print(f"S {tmp}",end="")
    for i in range(eStateSeedToSoil,eMaxState):
        tmp=ElmtConvTab[i].convert(tmp)
        if(debug):
            print(f" {tmp}", end="")
    if(debug):
        print("")
    return tmp



def saveResult(location,result,seed):
    debug=0
    if (result == 0):
        result = location
        if debug:
            print(f"first result:{result}")
    else:
        if (location < result):
            result = location
            if debug:
                print(f"new result:{result} ({seed})")
    return result

def dichotomise(indexMin, indexMax,seed,location):
    debug=0
    while ((indexMax - indexMin) > 1):
        range = indexMax - indexMin;
        test_seed = indexMin+int(range/2)
        test_location = testSeed(test_seed)
        diffLocation = test_location - location
        diffSeed = test_seed - seed
        if (diffLocation != diffSeed):
            indexMax = test_seed
        else:
            indexMin = test_seed
        if(debug):
            print(f"Dichotomy {indexMin},{indexMax}")
    return indexMax




    return min+int(range/2);
def getMin(seedRangeStart,seedRangeLenght,result):
    debug=0
    dicho=1
    nbSample = int(seedRangeLenght)

    indexMin=seedRangeStart
    seedRangeEnd=seedRangeStart+seedRangeLenght-1
    indexMax=seedRangeEnd

    while True:
        seed=indexMin
        location=testSeed(seed)
        result=saveResult(location, result,seed)
        if (debug):
            print(f"S={seed} L={location} iMin={indexMin}  iMax={indexMax}")
        if(indexMin>=indexMax):
            break
        if(dicho):
            indexMin=dichotomise(indexMin,indexMax,seed,location)
        else:
            indexMin +=1
        indexMax=seedRangeEnd

    return result

def getSeedList(lines,seeds_list,seeds_range):
    line=lines.pop(0)

    nbSeedRange=int(len(line.split(":")[1].strip().split(" "))/2)
    seeds_raw = line.split(":")[1].strip().split(" ")
    for num_seed in range(0,nbSeedRange):
        seedRangeStart=int(seeds_raw.pop(0))
        seedRangeLenght=int(seeds_raw.pop(0))
        seeds_list.append(seedRangeStart)
        seeds_range.append(seedRangeLenght)

if __name__ == '__main__':
    file = open('./5.txt', "r")
    debug=0
    lines = file.readlines()
    file.close()

    result = 0
    state = estateSeed
    ElmtConvTab=[0 for x in range(eMaxState)]


    seeds_list=[]
    seeds_range=[]
    getSeedList(lines,seeds_list,seeds_range)

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
    print(f"Part 1 : {result}")

    result=0;
    save_num_seed=0
    save_seed=0

    seeds_list_tmp = seeds_list.copy()
    seeds_range_tmp = seeds_range.copy()

    for num_seed in range(0,int(len(seeds_list))):
        seedRangeStart=int(seeds_list.pop(0))
        seedRangeLenght=int(seeds_range.pop(0))
        if(debug):
            print(f"range : {seedRangeStart} {seedRangeLenght}")
        result = getMin(seedRangeStart, seedRangeLenght,result)
    print(f"Part 2 : {result}")



