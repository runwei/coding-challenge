# example of program that calculates the number of tweets cleaned

import json
import sys

def cleantweets(input,output):
    numUnicodeline = 0
    fr = open(input, 'r')
    fw = open(output, 'w')
    for line in fr:
        data = json.loads(line)
        if 'created_at' in data and 'text' in data:
            datatime = data['created_at'].encode('ascii','ignore')
            datatext,flag = containUnicode(data['text'])
            if flag:
                numUnicodeline += 1
            fw.write("%s (timestamp: %s)\n"%(datatext,datatime))
    fw.write("\n%d tweets contained unicode.\n"%numUnicodeline)
    fr.close()
    fw.close()

def containUnicode(str):
    try:
        ret = str.encode('ascii')
    except UnicodeEncodeError:
        ret = str.encode('ascii','ignore')
        return ret,True
    else:
        return ret,False


if __name__ == "__main__":
    if len(sys.argv)>1:
        input = sys.argv[1]
        output = sys.argv[2]
    cleantweets(input,output)