import os
import operator
import math
import sys
from kmeans import *
from spicyStats import *
class Conference:
        def __init__(self, name, papers):
                self.count = 0.0
                self.papers = papers
		self.name = name
        def getAverages(self):
                output = [0]*len(self.papers[self.papers.keys()[0]])
                for i in range(len(self.papers[self.papers.keys()[0]])):
			for j in self.papers.keys():
#				print(j, len(self.papers[j]))
                        	output[i] += self.papers[j][i]
			output[i] /= self.count
                return output

def assignConfAttributes(Papers, PAA, N, conf):
        output = []
	data = {}
	index = 0
        #Year of Proceeding
        if (1 in N):
 #      print('assinging year of proceeding')
		for key, paper in Papers.items():
			if conf not in paper.conf:
				continue
		        if paper.pid not in data:
		        	data[paper.pid] = []
		        data[paper.pid].append(int(paper.year))
		index += 1
	#If 'vector machine' is a keyword of the paper (weight 10)
	if (2 in N):
	#       print('assining vector machine')
		checked = set()
       	 	for key, paper in Papers.items():
                	if conf not in paper.conf:
                        	continue
        	        if paper.pid not in data:
                	        data[paper.pid] = []
       		        data[paper.pid].append(0)
                	for keyword in paper.keywords:
                        	if 'world wide web' in keyword:
                                	data[paper.pid][index] = 20
		index += 1
        #If 'vector machine' is a keyword of the paper (weight 10)
        if (3 in N):
        #       print('assining vector machine')
                checked = set()
                for key, paper in Papers.items():
                        if conf not in paper.conf:
                                continue
                        if paper.pid not in data:
                                data[paper.pid] = []
                        data[paper.pid].append(0)
                        for keyword in paper.keywords:
                                if 'web search engine' in keyword:
                                        data[paper.pid][index] = 20
                index += 1
        #If 'vector machine' is a keyword of the paper (weight 10)
        if (4 in N):
        #       print('assining vector machine')
                checked = set()
                for key, paper in Papers.items():
                        if conf not in paper.conf:
                                continue
                        if paper.pid not in data:
                                data[paper.pid] = []
                        data[paper.pid].append(0)
                        for keyword in paper.keywords:
                                if 'data mining' in keyword:
                                        data[paper.pid][index] = 20
                index += 1

       	#Number of Authors who wrote the paper
        if (5 in N):
	#       print('assinging author count')
		checked = set()
		for paper in PAA:
	                if paper.pid not in Papers:
                                continue
                        if conf not in Papers[paper.pid].conf:
                                continue
	                if paper.pid not in data:
        	                data[paper.pid] = []
                	if paper.pid not in checked:
				data[paper.pid].append(0)
                               	checked.add(paper.pid)
	                data[paper.pid][index] += 1
		index += 1
	return data

def maxIndex(data):
	maxVal = 0
	index = 0
	for i in range(len(data)):
		if data[i] > maxVal:
			maxVal = data[i]
			index = i
	return index

def clusterOwnership(icdm, kdd, wsdm, www):
	checked = set()
	clusters = [0]*4
	for c in range(len(icdm)):
		temp = []
		temp.append(icdm[c])
		temp.append(kdd[c])
		temp.append(wsdm[c])
		temp.append(www[c])
		conf = maxIndex(temp)
		while conf in checked:
			temp[conf] = 0
			conf = maxIndex(temp)
		checked.add(conf)
		clusters[conf] = c
	return clusters
def confClustering(Papers, PAA, confs):
	data = {}
	centroids = []
	i = 0
	paperConf = {}
	counts = {}
	for paper in Papers:
		paperConf[paper] = Papers[paper].conf
	for conf in confs:
		data[conf] = Conference(conf,assignConfAttributes(Papers, PAA, [1,2,3,4,5],conf))
		data[conf].count += len(data[conf].papers)
		print(conf + ': ' + str(data[conf].count))
		centroids.append(data[conf].getAverages())
		print(centroids[i])
		counts[conf] = data[conf].count
		i += 1
	attributeData = assignAttributes(Papers, PAA, [1,2,3,4,5])
	results  = kMeans(attributeData, 4, 'euclidean', centroids)
	centroids = results[0]
	clusters = results[1]
	icdm = [0.0]*len(clusters)
	kdd = [0.0]*len(clusters)
	wsdm = [0.0]*len(clusters)
	www = [0.0]*len(clusters)
	i=0
	for cluster in clusters:
		for paper in cluster.papers:
			if paperConf[paper] == 'icdm':
				icdm[i] += 1	
			if paperConf[paper] == 'kdd':
				kdd[i] += 1	
			if paperConf[paper] == 'wsdm':
				wsdm[i] += 1	
			if paperConf[paper] == 'www':
				www[i] += 1
		icdm[i] = 100*(icdm[i]/counts['icdm'])	
		kdd[i] = 100*(kdd[i]/counts['kdd'])	
		wsdm[i] = 100*(wsdm[i]/counts['wsdm'])	
	#	www[i] = 100*(www[i]/cluster.count)
		www[i] = 100*(www[i]/counts['www'])
		print('===============')
		print('icdm: ' + str(icdm[i]))	
		print('kdd: ' + str(kdd[i]))	
		print('wsdm: ' + str(wsdm[i]))	
		print('www: ' + str(www[i]))	
		i+= 1

	ownership = clusterOwnership(icdm,kdd,wsdm,www)		

	print('Conference ICDM belongs to cluster ' + str(ownership[0]))
	print('Conference KDD belongs to cluster ' + str(ownership[1]))
	print('Conference WSDM belongs to cluster ' + str(ownership[2]))
	print('Conference WWW belongs to cluster ' + str(ownership[3]))
