import os
import operator
import math
import sys
from kmeans import *

class Conference:
        def __init__(self, x):
                self.count = 0.0
                self.papers = []

        def getAverages(self, centroids):
                if (self.count == 0):
                        return centroids
                output = [0]*len(self.data)
                for i in range(len(self.data)):
                        output[i] = self.data[i]/self.count
                return output


#Idea: find # of conferences, N, and run kmeans with N clusters. Also make the starting centroids 1 from each conference which is the average values of papers from that conference
#then compare final clusters to see how many papers remain in right conference
def confClustering(Papers, PAA):
	data = assignAttributes(Papers, PAA, [1,2,3], 'dict')
	for key, values in data.items():
		
