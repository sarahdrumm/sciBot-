import os
import operator
KEY = "matrix"

fa = open("./microsoft/PaperAuthorAffiliations.txt")
fp = open("./microsoft/Papers.txt")
papers = {}
authorCounts = {}
authorPaperCounts = {}
authorEntries = fa.readlines()
paperEntries = fp.readlines()
for line in authorEntries:
	words = line.split()
	paperID = words[0]
	authorID = words[1]
	if paperID in papers:
		if authorID not in papers[paperID]:
			papers[paperID].append(authorID)
	else:
			papers[paperID] = [authorID]
	if authorID in authorPaperCounts:
		authorPaperCounts[authorID] += 1
	else:
		authorPaperCounts[authorID] = 1

for line in paperEntries:
	words = line.split("\t")
	paperID = words[0]
	title = words[2]
	length = len(title)
	for a in papers[paperID]:
		if a in authorCounts:
			authorCounts[a] += length
		else:
			authorCounts[a] = length	

for a in authorCounts:
	authorCounts[a] /= authorPaperCounts[a]

for i in range(3):
	max1 = max(authorCounts.iteritems(), key=operator.itemgetter(1))[0]
	print (max1, authorCounts[max1])
	authorCounts[max1] = 0
