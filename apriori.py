import os
import operator
from itertools import *

def generateCandidates(F, K):
#	print('generating candidates', K)
	C = []
	keys = list(F.keys())
#	print('keys: ', keys)
	superSets = combinations(keys, 2)
	for s1 in superSets:
#		print('super: ', s1)
		valid = 1
		if K >1:
			s1 = s1[0] + s1[1]
			s1  = tuple(sorted(set(s1)))
#		if K == 2:
#			print('set: ', s1)
		if len(s1) != K+1 or s1 in C:
			continue
		subSets = combinations(s1, K)
		for s2 in subSets:
#			if K ==2:
#				print('sub: ', s2)
			if K == 1:
				s2 = s2[0]
			else:
				s2 = tuple(sorted(s2))
			if set(s2).issubset(set(F.keys())):
				print(s2, ' not in keys')
				valid = 0
				break
		if valid:
			C.append(s1)	
	return C
#	for key, value in F.items():
# takes in the potential frequent item sets and finds their support. Removes if support < minsup			
def countCandidates(C, transactions, minsup):
#	print('C: ',C)
#	print('counting candidates')
	counts = {}
	for item in C:
		for t in transactions:
			if set(item).issubset(set(transactions[t])):
				if item in counts:
					counts[item] +=1
				else:
					counts[item] = 1
	F = {k:v for (k,v) in counts.items() if v >= minsup}
#	print ('F: ', F)
	for key, value in sorted(F.items(), key=operator.itemgetter(1), reverse=True):
		print(key,value)
		break
	return F					

def getF(transactions, K, minsup):
	process = 0.0
        counts = {}
        for key, values  in transactions.items():
#		print (key,values)
		if len(values) < K+1:
                        continue
                superClass = combinations(values, K+1)
                for s1 in superClass:
			process += 1
			s1 = tuple(sorted(s1))
#			print(s1)
                        if s1 in counts:
                                counts[s1] += 1

			else:
				counts[s1] = 1
	for key, value in sorted(counts.items(), key=operator.itemgetter(1), reverse=True):
		print(key, value)
#		print(process)
		return {k:v for (k,v) in counts.items() if v >=minsup} 

#Task 4 - Apiori
def Apriori(PAA, minsup):
	#create all transactions (1 per paper)
	transactions = {}
	f1 = {}		#frequent item sets of size 1 (getting counts when creating transactions so we don't have to iterate over PAA twice)
	for item in PAA:
		if item.pid in transactions:
			transactions[item.pid].append(item.aid)
		else:
			transactions[item.pid] = [item.aid]
		if (item.aid) in f1:
			f1[(item.aid)] += 1
		else:
			f1[(item.aid)] = 1	

	C = []		#candidates
	F = {k:v for (k,v) in f1.items() if v >= minsup}		#frequent item sets of size k
	K = 1
	FIS = F		#all frequent item sets

	#while we have frequent itemsets do...
	while (len(F) != 0):
		#faster to generate F this way if |F| is large
		if len(F) > 200:
			F = getF(transactions, K, minsup)
		else:
			C = generateCandidates(F, K)
			F = countCandidates(C, transactions, minsup)
#		print (len(F))
		FIS.update(F)
		K += 1
	return FIS
