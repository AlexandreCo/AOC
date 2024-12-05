eNonelvl = 0
eWarnlvl = 1
eNoticelvl = 2
eInfolvl = 3
eVisulvl = 4
eDbglvl = 5

def isDebug(debug, lvl):
    if (debug >= lvl):
        return True
    else:
        return False