import os
import operator

class index:
	def __init__(self, folder, filename, pid, title):
		self.folder = folder
		self.filename = filename
		self.pid = pid
		self.title = title

	def display(self):
		print(self.folder, self.filename, self.pid, self.title)

class paper:
        def __init__(self, pid, title_case, title, year, conf, cid):
                self.pid = pid
		self.title_case = title_case
		self.title = title
		self.year = year
		self.conf = conf
		self.cid = cid

        def display(self):
                print(self.pid, self.title_case, self.title, self.year, self.conf, self.cid)

class paperKeyword:
        def __init__(self, pid, keyword):
                self.pid = pid
                self.keyword = keyword

        def display(self):
                print(self.pid,self.keyword)

class paperAuthorAffiliation:
        def __init__(self, pid, aid, fid, aff, sid):
                self.pid = pid
		self.aid = aid
		self.fid = fid
		self.aff = aff
		self.sid = sid
        def display(self):
                print(self.pid, self.aid, self.fid, self.aff, self.sid)

class author:
	def __init__(self, aid, name):
		self.aid = aid
		self.name = name
	def display(self):
		print(self.aid, self.name)


#Load in indexes#
fIndex = open("./microsoft/index.txt", "r")
indexEntries = []
for line in fIndex.readlines():
	words = line.split("\t")
	indexEntries.append(index(words[0], words[1], words[2], words[3]))
#Load in papers#
fPaper = open("./microsoft/Papers.txt", "r")
Papers = []
for line in fPaper.readlines():
        words = line.split("\t")
        Papers.append(paper(words[0], words[1], words[2], words[3], words[7], words[9]))
#Load in keywords
fKeywords = open("./microsoft/PaperKeywords.txt", "r")
paperKeywords = []
for line in fKeywords.readlines():
        words = line.split("\t")
        paperKeywords.append(paperKeyword(words[0], words[1]))
#Load in paperAuthorAffiliations
fPAA = open("./microsoft/PaperAuthorAffiliations.txt", "r")
PAA= []
for line in fPAA.readlines():
        words = line.split("\t")
        PAA.append(paperAuthorAffiliation(words[0], words[1], words[2], words[4], words[5]))
#Load in paperAuthorAffiliations
fAuthor = open("./microsoft/Authors.txt", "r")
Authors = []
for line in fAuthor.readlines():
        words = line.split("\t")
        Authors.append(author(words[0], words[1]))
print('finished loading files')
