import re

def spelledToNumber(line):
    line = line.replace(str("one"), "o1")
    line = line.replace(str("two"), "t2")
    line = line.replace(str("three"), "t3")
    line = line.replace(str("four"), "f4")
    line = line.replace(str("five"), "f5")
    line = line.replace(str("six"), "s6")
    line = line.replace(str("seven"), "s7")
    line = line.replace(str("eight"), "e8")
    line = line.replace(str("nine"), "n9")
    return line

def spelledToNumberRevers(line):
    line = line.replace(str("one")[::-1], "e1")
    line = line.replace(str("two")[::-1], "o2")
    line = line.replace(str("three")[::-1], "e3")
    line = line.replace(str("four")[::-1], "r4")
    line = line.replace(str("five")[::-1], "e5")
    line = line.replace(str("six")[::-1], "x6")
    line = line.replace(str("seven")[::-1], "n7")
    line = line.replace(str("eight")[::-1], "t8")
    line = line.replace(str("nine")[::-1], "e9")
    return line


def removeLetter(line) :
    return re.sub("[a-z]", "", line)

if __name__ == '__main__':
    file = open('./1.txt', "r")
    lines = file.readlines()
    file.close()
    sum = 0
    for rline in lines:
        # get first number
        line=rline.strip()
        line=spelledToNumber(line)
        line = removeLetter(line)
        first=int(line[0])

        line=rline [::-1].strip()
        line=spelledToNumberRevers(line)
        line = removeLetter(line)
        second=int(line[0])

        number = int(first) * 10 +int(second)
        sum += number
    print(sum)
