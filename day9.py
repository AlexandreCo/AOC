import re
import sys

eNonelvl=0
eWarnlvl=1
eNoticelvl=2
eInfolvl=3
eDbglvl=4

def isDebug(debug,lvl):
    if(debug>=lvl):
        return True
    else:
        return False

def getData(filename,part,debug):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    datas=[]
    for line in lines:
        datas.append(list(map(int, line.strip().split(" "))))

    lineslist = []
    i = 0
    for data in datas:
        ligne = []
        ligne.append(data)
        i += 1
        d = data
        while (True):
            c=d.copy()
            d, ret = derivative(c)
            if (ret == True):
                break
            ligne.append(d)

        lineslist.append(ligne)
    return lineslist
def derivative(values):
    new_data=[]
    ret=True
    v=values.pop(0)
    if(v):
        ret=False
    for val in values:
        new_data.append(val-v)
        v=val
        if (v):
            ret = False
    return new_data,ret

def integral(values):
    pv=values.pop()
    pv.append(0)

    for value in reversed(values):
        i=0
        tmp=[]

        tmp.append(value[0])
        for v in value:
            new=tmp[i]+pv[i]
            tmp.append(new)
            i += 1
        pv=tmp
    return tmp[len(tmp)-1]
def run(debug,lineslist):

    result=0
    i=0
    for linelist in lineslist:
        i+=1
        res=integral(linelist)
        #print(res)
        result+=res
    return result


if __name__ == '__main__':
    debug = eNonelvl
    #debug = eInfolvl
    filename = './9.txt'
    part=1
    linelists=getData(filename,part,debug)
    print(f"Part 1 : {run(debug,linelists)}")

    part+=1
    linelists=getData(filename,part,debug)
    print(f"Part 1 : {run(debug,linelists)}")
