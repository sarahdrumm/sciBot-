import os
import operator
from itertools import *
from apriori import Apriori
from kmeans import *
from spicyStats import *
from confClustering import *
from entityExtraction import *
from entityTyping import *
from entityLabeling import *
from testMine import *
from entityFP import *
from naiveBayes import *

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
		self.confs = set()
		self.keywords = set()
		self.authors = set()
		self.confs.add(conf)
		self.path = ''

        def display(self):
                print(self.pid, self.title_case, self.title, self.year, self.conf, self.cid)

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
fPaper = open("./microsoft/Papers.txt", "r")
#use of a dictioanry removes duplicate values
Papers = {}
for line in fPaper.readlines():
        words = line.split("\t")
        #remove papers not in our given conferences
        if words[7] not in ['icdm', 'kdd', 'wsdm', 'www']:
                continue
        if words[0] not in Papers:
                Papers[words[0]] = paper(words[0], words[1], words[2], words[3], words[7], words[9])
        elif words[7] not in Papers[words[0]].confs:
                Papers[words[0]].confs.add(words[7])
#Load in indexes#
fIndex = open("./microsoft/index.txt", "r")
indexEntries = []
for line in fIndex.readlines():
	words = line.split("\t")
	#removes entries with null values
	if '' in words:
		continue
	if words[2] in Papers:
		indexEntries.append(index(words[0], words[1], words[2], words[3]))
		Papers[words[2]].path = './text/' + words[0] + '/' + words[1]
#Load in keywords
fKeywords = open("./microsoft/PaperKeywords.txt", "r")
for line in fKeywords.readlines():
        words = line.split("\t")
	if '' in words:
		continue
	if words[0] in Papers:
		#use of a set removes duplicate values
	        Papers[words[0]].keywords.add(words[1])
#Load in Authors
fAuthor = open("./microsoft/Authors.txt", "r")
Authors = {}
for line in fAuthor.readlines():
        words = line.split("\t")
	if '' in words:
		continue
	if words[0] not in Authors:
		Authors[words[0]] = author(words[0], words[1])
#Load in paperAuthorAffiliations
fPAA = open("./microsoft/PaperAuthorAffiliations.txt", "r")
PAA= []
for line in fPAA.readlines():
        words = line.split("\t")
	#remove entries with null values
	if '' in words:
		continue
	#remove invalid entries (i.e. must exist in Papers to exist in PAA)
	if words[0] in Papers and words[1] in Authors:
        	PAA.append(paperAuthorAffiliation(words[0], words[1], words[2], words[4], words[5]))
		#use of a set removes duplicate authors
		Papers[words[0]].authors.add(words[1])
print('finished loading files')

print('\nTask 1 - Data Cleaning, statistics, attribute assigning, visualization')
Papers = finalClean(Papers)
spicyStats(Papers)
#[1,2,3] array indicates we want to use all 3 attributes for our data
attributeData = assignAttributes(Papers,PAA, [1,2,3,4,5])

print('\nTask 2 - Entity mining: Candidate generation and quality assessment')
print('=======================')
#entityExtraction(Papers)
print('=======================')

print('\nTask 3 - Entity typing')
print('=======================')
#entityTyping(Papers)
#entityLabeling()
print('=======================')

print('\nTask 4 - Frequent Patern Mining (Apriori)')
print('=======================')
#Apriori(PAA, Papers, 5)
print('=======================')

print('\nTask 5 - Problem-method association mining')
print('=======================')
#Phrases = entiMining(Papers)
#Problems = []
#Methods = []
#fProb = open("./problem.txt", "r")
#for line in fProb.readlines():
#        words = line.split("\n")
#	Problems.append(words[0])
#fMeth = open("./method.txt", "r")
#for line in fMeth.readlines():
#        words = line.split("\n")
#        Methods.append(words[0])
#AprioriEntity(Phrases, Problems, Methods, 10)

print('=======================')

print('\nTask 6 - Naive Bayes')
print('=======================')
naiveBayes(Papers, ['kdd','wsdm', 'www', 'icdm'], ['collaborative filtering', 'data mining'])
naiveBayes(Papers, ['wsdm', 'www', 'icdm', 'kdd'], ['latent dirichlet allocation', 'expectation maximization'])
naiveBayes(Papers, ['kdd','wsdm','www', 'icdm'], ['support vector machine', 'data mining'])
naiveBayes(Papers, ['kdd', 'wsdm','icdm' ,'www'], ['support vector machine', 'data mining'])
print('=======================')

print('\nTask 7 - KMeans clustering')
print('=======================')
#call Kmeans with 4 clusters and euclidean distance metric
#kMeans(attributeData, 4, 'euclidean', 'random')
print('=======================')

print('\nTask 8 - Conference Clustering')
print('=======================')
#confClustering(Papers, PAA, ['icdm', 'kdd', 'wsdm', 'www'])
print('=======================')

