import os
import operator
import math
import sys
from random import *
class Cluster:
	def __init__(self, x):
		self.count = 0.0
		self.data = [0]*x
		self.papers = set()
	def getAverages(self, centroids):
		if (self.count == 0):
			return centroids
		output = [0]*len(self.data)
		for i in range(len(self.data)):
			output[i] = self.data[i]/self.count
		return output

def Manhattan(data, centroids):
	output = [0]*len(centroids)
	for i in range(len(centroids)):
		dist = 0
		for j in range(len(data)):
			dist += abs(centroids[i][j] - data[j])
		output[i] = dist
#	print('distances: ',output)
	return output

def Euclidean(data, centroids):
	output = [0]*len(centroids)
	for i in range(len(centroids)):
		dist = 0
		for j in range(len(data)):
			dist += pow(centroids[i][j] - data[j], 2)
		dist = math.sqrt(dist)
		output[i] = dist
#	print('distances: ', output)
	return output


def kMeans(data, K, distMetric, C):
	centroids = []
	if C == 'random':
		for i in range(K):
			randInt = randint(0,len(data)-1)
			centroids.append(data[data.keys()[randInt]])
	else:
		centroids = C
	distances = [0]*K	#array to compute distance from 1 point to each centroid
	clusters = []	
	for i in range(K):
		clusters.append(Cluster(len(data[data.keys()[0]])))
	error = 10
	while error > 1:
		for i in range(len(clusters)):
			clusters[i].count = 0.0
			clusters[i].data = [0]*len(data[data.keys()[0]])
			clusters[i].papers = set()
		for i, paper in data.items():
			if (distMetric == 'manhattan'):
				distances = Manhattan(data[i], centroids)
			elif (distMetric == 'euclidean'):
				distances = Euclidean(data[i], centroids)
			
			#find which centroid has the smallest distance to the point
			dMin = sys.maxint
			c = 0
			#find which cluster point data[i] belongs to (aka index of the min of distances)
			for d in range(len(distances)):
				if distances[d] < dMin:
					dMin = distances[d]
					c = d
			#add this points attribute value to the cluster it belongs to
			for j in range(len(data[i])):
				clusters[c].data[j] += data[i][j]
			clusters[c].count += 1
			clusters[c].papers.add(i)
#			print('point ', i, 'cluster',c)
		newCentroids = [0]*K
		for i in range(K):
			newCentroids[i] = clusters[i].getAverages(centroids[i])
#			print(i, newCentroids[i])
		error = 0
		for i in range(K):
			for j in range(len(data[data.keys()[0]])):
				error += abs(centroids[i][j] - newCentroids[i][j])
#		print(error)
		centroids = newCentroids			
	for k in range(K):
		print('Cluster: ' + str(k))
		print(centroids[k]) 
		print('Cluster count: ' + str(clusters[k].count) + ', ' + str(len(clusters[k].papers)))
	return [centroids, clusters]

#C = [[4,3,0],[11,20,7],[7,12,3]]
#inputData = [[4,2,1], [15,22,5], [8,2,5], [11,17,14], [1,20,3]]

#kMeans(inputData, 3, 'euclidean')
