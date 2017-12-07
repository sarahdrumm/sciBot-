import os
import operator
from itertools import *
from testMine import *

def entityPMRelations(transactions, P, M, K, minsup):
        counts = {}
        for key, values  in transactions.items():
		problems = values[1]
		methods = values[0]
#		print (key,problems, methods)
		if len(problems) < K or len(methods) < K:
                        continue
                superClass = list(product(problems, methods))
                for s1 in superClass:
#			print(s1)
                        if s1 in counts:
                                counts[s1] += 1

			else:
				counts[s1] = 1
	ixx = 0
	for key, value in sorted(counts.items(), key=operator.itemgetter(1), reverse=True):
		print(key, value)
#		print(process)
		if ixx > 5:
			break
		ixx+=1
	return {k:v for (k,v) in counts.items() if v >=minsup} 

#Task 4 - Apiori
def AprioriEntity(Phrases, Problems, Methods, minsup):
	#come up with Problem, Method counts of size 1
	p1 = {}
	m1 = {}
	transactions = {}
	for phrase, track in Phrases.items():
		if phrase == 'operating system':
			print(phrase, phrase in Problems, phrase in Methods)
		for pid in track.paperids:
			if pid not in transactions:
				transactions[pid] = []
				temp = []
				temp2 = []
				transactions[pid].append(temp)
				transactions[pid].append(temp2)
			if pid in transactions:
				if phrase in Problems:
					transactions[pid][1].append(phrase)
				elif phrase in Methods:
					transactions[pid][0].append(phrase)
		if phrase in Problems:
			p1[phrase] = len(track.paperids)
		elif phrase in Methods:
			m1[phrase] = len(track.paperids)
		
	C = []		#candidates
	P = {k:v for (k,v) in p1.items() if v >= minsup}		#frequent item sets of size k
	M = {k:v for (k,v) in m1.items() if v >= minsup}		#frequent item sets of size k
	K = 1
	F = entityPMRelations(transactions, P, M, K, minsup)
	return F



temp = '''Phrases = {}
Phrases['dog'] = tracking()
Phrases['dog'].count = 3
Phrases['dog'].paperids.add('1')
Phrases['dog'].paperids.add('3')
Phrases['dog'].paperids.add('7')
Phrases['cat'] = tracking()
Phrases['cat'].count = 4
Phrases['cat'].paperids.add('2')
Phrases['cat'].paperids.add('4')
Phrases['cat'].paperids.add('5')
Phrases['cat'].paperids.add('21')
Phrases['walk'] = tracking()
Phrases['walk'].count = 2
Phrases['walk'].paperids.add('1')
Phrases['walk'].paperids.add('7')
Phrases['eat'] = tracking()
Phrases['eat'].count = 3
Phrases['eat'].paperids.add('1')
Phrases['eat'].paperids.add('4')
Phrases['eat'].paperids.add('21')
Phrases['eat'] = tracking()
Phrases['eat'].count = 3
Phrases['eat'].paperids.add('1')
Phrases['eat'].paperids.add('4')
Phrases['eat'].paperids.add('21')
Problems = ['eat', 'walk']
Methods = ['dog', 'cat']
AprioriEntity(Phrases, Problems, Methods,  2)
'''
