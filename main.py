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



def saveResult(location,result,seed,num_seed):
    debug=0
    if (result == 0):
        result = location
        save_seed = seed
        save_num_seed = num_seed
        if debug:
            print(f"first result:{result} at seed {seed} (seed range {num_seed})")
    else:
        if (location < result):
            result = location
            save_seed = seed
            save_num_seed = num_seed
            if debug:
                print(f"new result:{result} at seed {seed} (seed range {num_seed})")
    return result, save_num_seed, save_seed

def dicotomise(min, max):
    range=max-min;
    return min+int(range/2);
def getMin(seedRangeStart,seedRangeLenght,result, save_num_seed, save_seed):
    nbSample = int(seedRangeLenght)

    indexMin=seedRangeStart
    seedRangeEnd=seedRangeStart+seedRangeLenght-1
    indexMax=seedRangeEnd

    while True:
        seed=indexMin
        location=testSeed(seed)
        saveResult(location,result, save_num_seed, save_seed)
        print(seed,location)

        print(indexMin, indexMax)

        while ((indexMax-indexMin)>1):
            test_seed=dicotomise(indexMin, indexMax)
            test_location=testSeed(test_seed)
            diffLocation=test_location-location
            diffSeed=test_seed - seed
            if(diffLocation!=diffSeed):
                indexMax=test_seed
            else:
                indexMin=test_seed
            print(diffLocation, diffSeed,indexMin,indexMax)
        indexMin=indexMax
        indexMax=seedRangeEnd








    return result, save_num_seed, save_seed

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
    file = open('./5-tiny.txt', "r")
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

    result=0;
    save_num_seed=0
    save_seed=0

    seeds_list_tmp = seeds_list.copy()
    seeds_range_tmp = seeds_range.copy()

    for num_seed in range(0,int(len(seeds_list))):
        seedRangeStart=int(seeds_list.pop(0))
        seedRangeLenght=int(seeds_range.pop(0))
        result, save_num_seed, save_seed = getMin(seedRangeStart, seedRangeLenght,result, save_num_seed, save_seed)
    print(f"result : {result} at seed {save_seed} of range {save_num_seed}")



