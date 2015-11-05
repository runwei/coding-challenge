import json
import sys
import re

def cleantweets(input,output):
    numUnicodeline = 0
    fr = open(input, 'r')
    fw = open(output, 'w')
    for line in fr:
        data = json.loads(line)
        if 'created_at' in data and 'text' in data:
            datatime = data['created_at'].encode('ascii','ignore')
            datatext,flag = containUnicode(data['text'])
            datatext = replaceChar(datatext)
            if flag:
                numUnicodeline += 1
            fw.write("%s (timestamp: %s)\n"%(datatext,datatime))
    fw.write("\n%d tweets contained unicode.\n"%numUnicodeline)
    fr.close()
    fw.close()

## check if string has unicode and return the ascii version
def containUnicode(str):
    try:
        ret = str.encode('ascii')
    except UnicodeEncodeError:
        ret = str.encode('ascii','ignore')
        return ret,True
    else:
        return ret,False

## replace the escape characters
def replaceChar(s):
    s = s.replace('\n',' ').replace('\t', ' ')
    s = re.sub('\s\s+',' ', s)
    return s

if __name__ == "__main__":
    if len(sys.argv)>1:
        input = sys.argv[1]
        output = sys.argv[2]
    else:
        input = "../tweet_input/tweets.txt"
        output = "../tweet_output/ft1.txt"
    cleantweets(input,output)