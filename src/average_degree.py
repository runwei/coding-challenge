# example of program that calculates the average degree of hashtags
import json
import collections
from re import findall
from datetime import datetime
import time
import sys

class Socialgraph:
    def __init__(self,fileread,filewrite):
        self.nodeLink = dict() # a 2d dictionary, keys are nodeid, value is time
        self.curtime = 0
        self.fileread = open(fileread, 'r')
        self.filewrite = open(filewrite,'w')
        self.log = collections.deque() # the moving window of {time:hashtags}

    def processfile(self):
        for line in self.fileread:
            data = json.loads(line)
            if 'text' in data and 'created_at' in data:
                texttime = data['created_at'].encode('ascii','ignore')
                self.curtime = time.mktime(datetime.strptime(texttime,'%a %b %d %H:%M:%S +0000 %Y').timetuple())
                taglist = self.extractHashtag(data['text'].encode('ascii','ignore'))
                self.log.append({'time': self.curtime,'taglist':taglist})
                self.groupConnect(taglist)
                self.removeLogs()
                self.calAvgDegree()

## Go through the log and disconnect links until curtime-60seconds
    def removeLogs(self):
        while len(self.log) !=0:
            elem = self.log[0]
            if elem['time']<self.curtime-60:
                self.groupDisconnect(elem['taglist'])
                self.log.popleft()
            else:
                break

## Extract a list of hashtags in a certain tweet text
    def extractHashtag(self,datatext):
        return findall(r'#\w*', datatext.lower())

## Connect a group of hashtags altogether
    def groupConnect(self,taglist):
        length = len(taglist)
        if length >= 2:
            for i in xrange(0,length-1):
                for j in xrange(i+1,length):
                    if taglist[i]!= taglist[j]:
                        self.Connect(taglist[i],taglist[j])

## Disconnect a group of hashtags if the links between them has not been updated for 60 seconds
    def groupDisconnect(self,taglist):
        length = len(taglist)
        if length >= 2:
            for i in xrange(0,length-1):
                for j in xrange(i+1,length):
                    if taglist[i]!= taglist[j]:
                        self.Disconnect(taglist[i],taglist[j])

# Caluculate the average degree in the social graph
    def calAvgDegree(self):
        if len(self.nodeLink) == 0:
            avgdegree = 0.0
        else:
            sumdegree = 0.0
            for elem in self.nodeLink:
                sumdegree +=len(self.nodeLink[elem])
            avgdegree = sumdegree/len(self.nodeLink)
        self.filewrite.write("%.2f\n"%avgdegree)

# Connect two hashtags in the social graph
    def Connect(self,word1,word2):
        if word1 not in self.nodeLink:
            self.nodeLink[word1] = {word2:self.curtime}
        else:
            self.nodeLink[word1][word2] = self.curtime
        if word2 not in self.nodeLink:
            self.nodeLink[word2] = {word1:self.curtime}
        else:
            self.nodeLink[word2][word1] = self.curtime

# Disconnect two hashtags in the social graph if the link has not been updated for 60 seconds
    def Disconnect(self,word1,word2):
        if word1 in self.nodeLink:
            if word2 in self.nodeLink[word1] and self.nodeLink[word1][word2]<self.curtime-60:
                del self.nodeLink[word1][word2]
                if len(self.nodeLink[word1]) == 0:
                    del self.nodeLink[word1]
        if word2 in self.nodeLink:
            if word1 in self.nodeLink[word2] and self.nodeLink[word2][word1]<self.curtime-60:
                del self.nodeLink[word2][word1]
                if len(self.nodeLink[word2]) == 0:
                    del self.nodeLink[word2]

    def __del__(self):
        self.fileread.close()
        self.filewrite.close()

if __name__ == '__main__':
    if len(sys.argv)>1:
        input = sys.argv[1]
        output = sys.argv[2]
    else:
        input = "../tweet_input/tweets.txt"
        output = "../tweet_output/ft2.txt"
    sg = Socialgraph(input,output)
    sg.processfile()