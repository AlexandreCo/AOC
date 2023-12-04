import re

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file = open('./1.txt', "r")
    lines = file.readlines()
    file.close()
    sum=0
    for rline in lines:
        line=rline
        line = re.sub("[a-z]", "", line)
        number=(int(line[0])*10+int(line[len(line)-2]));
        sum+=number
        print(rline,line,line[0],line[len(line)-2],number,sum)



# 54644	sans sub
# 52963	avec sub