import os
import operator
KEY = "matrix"

fa = open("./microsoft/PaperAuthorAffiliations.txt")

f = open("./microsoft/PaperKeywords.txt", "r")
entries = f.readlines()
counts = {}
papers = {}
authorCounts = {}
paperDupPrevent = []
authorEntries = fa.readlines()
for line in authorEntries:
	words = line.split()
	paperID = words[0]
	authorID = words[1]
	if paperID in papers:
		if authorID not in papers[paperID]:
			papers[paperID].append(authorID)
	else:
			papers[paperID] = [authorID]

for line in entries:
	words = line.split()
	paperID = words[0]
	toAdd = 0

#	if paperID in paperDupPrevent:
#		continue
#	else:
#		paperDupPrevent.append(paperID)
	for w in words:
		if w == 'matrix':
			toAdd = 1
			if paperID in counts:
				counts[paperID] += 1
			else:
				counts[paperID] = 1
	if toAdd == 1:
	#	print ("adding to author counts")
		for a in papers[paperID]:
			if a in authorCounts:
				authorCounts[a] += counts[paperID]
			else:
				authorCounts[a] = counts[paperID]	

for i in range(3):
	max1 = max(authorCounts.iteritems(), key=operator.itemgetter(1))[0]
	print (max1, authorCounts[max1])
	authorCounts[max1] = 0
