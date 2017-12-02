#!/usr/bin/python
#from numpy import log2
import math
import random

basePath = '../../'

def SimpleEntityExtraction():
	paperid_path = []
	fr = open(basePath + 'microsoft/index.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split('\t')
		paperid = arr[2]
		path = basePath + 'text/'+arr[0]+'/'+arr[1]+'.txt'
		paperid_path.append([paperid,path])
	fr.close()
	phrase2count = {}
	for [paperid,path] in paperid_path[0]:
		fr = open(path,'rb')
		for line in fr:
			arr = line.strip('\r\n').split(' ')
			n = len(arr)
			if n < 5: continue
			for i in range(0,n-2):
				if arr[i] == '(' and arr[i+2] == ')':
					abbr = arr[i+1]
					l = len(abbr)
					if l > 1 and abbr.isalpha():
						if i >= l and abbr.isupper():
							isvalid = True
							for j in range(0,l):
								if not abbr[l-1-j].lower() == arr[i-1-j][0].lower():
									isvalid = False
							if isvalid:
								phrase = ''
								for j in range(0,l):
									phrase = arr[i-1-j]+' '+phrase
								phrase = phrase[0:-1].lower()
								if not phrase in phrase2count:
									phrase2count[phrase] = 0
								phrase2count[phrase] += 1
						if i >= l-1 and abbr[-1] == 's' and arr[i-1][-1] == 's' and abbr[0:-1].isupper():
							isvalid = True
							for j in range(1,l):
								if not abbr[l-1-j].lower() == arr[i-j][0].lower():
									isvalid = False
							if isvalid:
								phrase = ''
								for j in range(1,l):
									phrase = arr[i-j]+' '+phrase
								phrase = phrase[0:-1].lower()
								if not phrase in phrase2count:
									phrase2count[phrase] = 0
								phrase2count[phrase] += 1
		fr.close()
	fw = open('phrase2count.txt','w')
	for [phrase,count] in sorted(phrase2count.items(),key=lambda x:-x[1]):
		fw.write(phrase+'\t'+str(count)+'\n')
	fw.close()

def SimpleAttributeExtraction():
	paperid_path = []
	fr = open(basePath + 'microsoft/index.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split('\t')
		paperid = arr[2]
		path = basePath + 'text/'+arr[0]+'/'+arr[1]+'.txt'
		paperid_path.append([paperid,path])
	fr.close()
	index,nindex = [{}],1 # phrase's index
	fr = open('phrase2count.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split('\t')
		phrase = arr[0]
		words = phrase.split(' ')
		n = len(words)
		if n > nindex:
			for i in range(nindex,n):
				index.append({})
			nindex = n
		temp = index[n-1]
		if n > 1:
			for i in range(0,n-1):
				word = words[i]
				if not word in temp:
					temp[word] = {}
				temp = temp[word]
			word = words[n-1]
		else:
			word = words[0]
		temp[word] = phrase
	fr.close()
	fw = open('paper2attributes.txt','w')
	for [paperid,path] in paperid_path:
		attributeset = set()
		fr = open(path,'rb')
		for line in fr:
			words = line.strip('\r\n').split(' ')
			wordslower = line.strip('\r\n').lower().split(' ')
			l = len(words)
			i = 0
			while i < l:
				isvalid = False
				for j in range(min(nindex,l-i),0,-1):
					temp = index[j-1]
					k = 0
					while k < j and i+k < l:
						tempword = wordslower[i+k]
						if not tempword in temp: break
						temp = temp[tempword]
						k += 1
					if k == j:
						phrase = temp
						attributeset.add(phrase)
						isvalid = True
						break
				if isvalid:
					i += j
					continue
				i += 1
		fr.close()
		if len(attributeset) == 0: continue
		s = ''
		for attribute in sorted(attributeset):
			s += ','+attribute
		fw.write(paperid+'\t'+s[1:]+'\n')
	fw.close()

def SimpleLabelExtraction():
	paperid2conf = {}
	fr = open(basePath + 'microsoft/Papers.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split('\t')
		paperid,conf = arr[0],arr[7]
		paperid2conf[paperid] = conf
	fr.close()
	fw = open('paper2attributes2label.txt','w')
	fr = open('paper2attributes.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split('\t')
		paperid = arr[0]
		if not paperid in paperid2conf: continue
		conf = paperid2conf[paperid]
		fw.write(arr[0]+'\t'+conf+'\t'+arr[1]+'\n')
	fr.close()
	fw.close()

def Entropy(n,values):
	ret = 0.0
	for value in values:
		p_i = 1.0*value/n
		if not p_i == 0:
			ret += -1.0*p_i*math.log(p_i,2)
	p_i = 1.0*(n-sum(values))/n
	if not p_i == 0:
		ret += -1.0*p_i*math.log(p_i,2)
	return ret

def Gini(n,values):
	ret = 1.0
	for value in values:
		p_i = 1.0*value/n
		ret -= p_i*p_i
	p_i = 1.0*(n-sum(values))/n
	ret -= p_i*p_i
	return ret

def Output(entry):
	print entry[0],0.001*int(1000.0*entry[1][0]),0.001*int(1000.0*entry[1][1]),entry[2], \
		0.001*int(1000.0*entry[2][0]/(entry[2][0]+entry[2][1])), \
		0.001*int(1000.0*entry[2][2]/(entry[2][2]+entry[2][3]))

def OutputStr(entry):
	print entry[0],entry[1][0],entry[1][1],entry[2]

def DecisionTreeFirstFeature():
	positive = 'kdd' # SIGKDD Conference on Knowledge Discovery and Data Mining
	paper2label,paper2attributes,attribute2papers = {},{},{}
	fr = open('paper2attributes2label.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split('\t')
		paper = arr[0]
		label = (arr[1] == positive)
		paper2label[paper] = label
		attributes = arr[2].split(',')
		paper2attributes[paper] = attributes
		for attribute in attributes:
			if not attribute in attribute2papers:
				attribute2papers[attribute] = []
			attribute2papers[attribute].append(paper)
	fr.close()

	nY,nYpos = 0,0
	for [paper,label] in paper2label.items():
		nY += 1
		if label: nYpos += 1
	print '----- -----'
	print 'All','KDD','NotKDD'
	print nY,nYpos,nY-nYpos,0.001*int(1000.0*nYpos/nY)
	print ''
	HY = Entropy(nY,[nYpos])
	GiniY = Gini(nY,[nYpos])

	attribute_metrics = []
	for [attribute,papers] in attribute2papers.items():
		nXyesY = len(papers)
		nXnoY = nY-nXyesY
		nXyesYpos = 0
		for paper in papers:
			label = paper2label[paper]
			if label: nXyesYpos += 1
		nXnoYpos = nYpos-nXyesYpos
		HXyesY = 1.0*nXyesY/nY * Entropy(nXyesY,[nXyesYpos])
		HXnoY = 1.0*nXnoY/nY * Entropy(nXnoY,[nXnoYpos])
		InfoGain = HY-(HXyesY+HXnoY)

		GiniXyesY = 1.0*nXyesY/nY * Gini(nXyesY,[nXyesYpos])
		GiniXnoY = 1.0*nXnoY/nY * Gini(nXnoY,[nXnoYpos])
		DeltaGini = GiniY-(GiniXyesY+GiniXnoY)
		
		attribute_metrics.append([attribute,[InfoGain,DeltaGini],[nXyesYpos,nXyesY-nXyesYpos,nXnoYpos,nXnoY-nXnoYpos]])

	bestattributeset = set()

	print '----- First Feature to Select in ID3: Information Gain -----'
	OutputStr(['Attribute',['InfoGain','DeltaGini'],['HasWord & KDD','HasWord & NotKDD','NoWord & KDD','NoWord & NotKDD']])
	sorted_attribute_metrics = sorted(attribute_metrics,key=lambda x:-x[1][0])
	for i in range(0,5):
		Output(sorted_attribute_metrics[i])
		bestattributeset.add(sorted_attribute_metrics[i][0])
	print ''

	print '----- First Feature to Select in CART: Delta Gini index -----'
	OutputStr(['Attribute',['InfoGain','DeltaGini'],['HasWord & KDD','HasWord & NotKDD','NoWord & KDD','NoWord & NotKDD']])
	sorted_attribute_metrics = sorted(attribute_metrics,key=lambda x:-x[1][1])
	for i in range(0,5):
		Output(sorted_attribute_metrics[i])
		bestattributeset.add(sorted_attribute_metrics[i][0])
	print ''

	fw = open('bestattributes.txt','w')
	for attribute in sorted(bestattributeset):
		fw.write(attribute+'\n')
	fw.close()

def NaiveBayes():
	positive = 'kdd' # SIGKDD Conference on Knowledge Discovery and Data Mining
	bestattributeset = set()
	fr = open('bestattributes.txt','rb')
	for line in fr:
		attribute = line.strip('\r\n')
		bestattributeset.add(attribute)
	fr.close()

	paper2label,paper2attributes,attribute2papers = {},{},{}
	fr = open('paper2attributes2label.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split('\t')
		attributeset = set(arr[2].split(','))
		selectedattributeset = bestattributeset & attributeset
#		if len(selectedattributeset) < 2 or len(selectedattributeset) > 4: continue
		paper = arr[0]
		label = (arr[1] == positive)
		paper2label[paper] = label
		paper2attributes[paper] = sorted(selectedattributeset)
		for attribute in selectedattributeset:
			if not attribute in attribute2papers:
				attribute2papers[attribute] = []
			attribute2papers[attribute].append(paper)
	fr.close()

	for [paper,attributes] in paper2attributes.items():
		print paper,attributes

	nY,nYpos = 0,0
	for [paper,label] in paper2label.items():
		nY += 1
		if label: nYpos += 1
	print ''
	print '----- -----'
	print 'All','KDD','NotKDD'
	print nY,nYpos,nY-nYpos,0.001*int(1000.0*nYpos/nY)
	print '----- Prior Probability -----'
	PYesPrior = 1.0*nYpos/nY
	PNoPrior = 1.0*(nY-nYpos)/nY
	print 'P(KDD) = ',0.001*int(1000.0*PYesPrior)
	print 'P(NotKDD) = ',0.001*int(1000.0*PNoPrior)
	print ''

	allpapers = paper2label.keys()
	random.shuffle(allpapers)
	for i in range(0,5):
		paper = allpapers[i]
		print '----- Paper ',i,':',paper,'-->',paper2label[paper],' -----'
		attributes = paper2attributes[paper]
		print '----- Likelihood -----'
		PYesLikelihoodAll = 1.0
		PNoLikelihoodAll = 1.0
		for [attribute,papers] in attribute2papers.items():
			if attribute in attributes:
				# P(word=yes|KDD), P(word=yes|NotKDD)
				nYesLikelihood = 0
				nNoLikelihood = 0
				for [paper,label] in paper2label.items():
					if paper in papers:
						if label: nYesLikelihood += 1
						else: nNoLikelihood += 1
				PYesLikelihood = 1.0*nYesLikelihood/nYpos
				PNoLikelihood = 1.0*nNoLikelihood/(nY-nYpos)
				PYesLikelihoodAll *= PYesLikelihood
				PNoLikelihoodAll *= PNoLikelihood
			else:
				# P(word=no|KDD), P(word=no|NotKDD)
				nYesLikelihood = 0
				nNoLikelihood = 0
				for [paper,label] in paper2label.items():
					if not paper in papers:
						if label: nYesLikelihood += 1
						else: nNoLikelihood += 1
				PYesLikelihood = 1.0*nYesLikelihood/nYpos
				PNoLikelihood = 1.0*nNoLikelihood/(nY-nYpos)
				PYesLikelihoodAll *= PYesLikelihood
				PNoLikelihoodAll *= PNoLikelihood
		print 'P(X|KDD) = ',0.001*int(1000.0*PYesLikelihoodAll)
		print 'P(X|NotKDD) = ',0.001*int(1000.0*PNoLikelihoodAll)
		print '----- Posteriori Probability -----'
		PYesPost = PYesPrior*PYesLikelihoodAll
		PNoPost = PNoPrior*PNoLikelihoodAll
		print 'P(KDD|X) ~ P(X|KDD)P(KDD)',0.0001*int(10000.0*PYesPost)
		print 'P(NotKDD|X) ~ P(X|NotKDD)P(NotKDD)',0.0001*int(10000.0*PNoPost)
		print '--> Prediction:',(PYesPost > PNoPost)
		print ''

SimpleEntityExtraction()
SimpleAttributeExtraction()
SimpleLabelExtraction()

DecisionTreeFirstFeature()

NaiveBayes()


