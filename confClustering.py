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
                        	if 'vector machine' in keyword:
                                	data[paper.pid][index] = 10
		index += 1
       	#Number of Authors who wrote the paper
        if (3 in N):
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

#Idea: find # of conferences, N, and run kmeans with N clusters. Also make the starting centroids 1 from each conference which is the average values of papers from that conference
#then compare final clusters to see how many papers remain in right conference
def confClustering(Papers, PAA, confs):
	data = {}
	centroids = []
	i = 0
	paperConf = {}
	for paper in Papers:
		paperConf[paper] = Papers[paper].conf
	for conf in confs:
		data[conf] = Conference(conf,assignConfAttributes(Papers, PAA, [1,2,3],conf))
		data[conf].count += len(data[conf].papers)
		print(conf + ': ' + str(data[conf].count))
		centroids.append(data[conf].getAverages())
		print(centroids[i])
		i += 1
	attributeData = assignAttributes(Papers, PAA, [1,2,3])
	results  = kMeans(attributeData, 4, 'euclidean', centroids)
	centroids = results[0]
	clusters = results[1]
	for cluster in clusters:
		icdm = 0.0
		kdd = 0.0
		wsdm = 0.0
		www = 0.0
		for paper in cluster.papers:
			if paperConf[paper] == 'icdm':
				icdm += 1	
			if paperConf[paper] == 'kdd':
				kdd += 1	
			if paperConf[paper] == 'wsdm':
				wsdm += 1	
			if paperConf[paper] == 'www':
				www += 1
		print('%icdm: ', str(100*(icdm/cluster.count)))	
		print('%kdd: ', str(100*(kdd/cluster.count)))	
		print('%wsdm: ', str(100*(wsdm/cluster.count)))	
		print('%www: ', str(100*(www/cluster.count)))	
