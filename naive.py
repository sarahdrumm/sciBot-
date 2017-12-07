#!/usr/bin/python
import math
import random

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
		paper = arr[0]
		label = (arr[1] == positive)
		paper2label[paper] = label
		paper2attributes[paper] = sorted(selectedattributeset)
		for attribute in selectedattributeset:
			if not attribute in attribute2papers:
				attribute2papers[attribute] = []
			attribute2papers[attribute].append(paper)
	fr.close()

#	for [paper,attributes] in paper2attributes.items():
#		print paper,attributes

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

NaiveBayes()
