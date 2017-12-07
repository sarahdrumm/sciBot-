import os
import operator
from itertools import *
#import plotly.plotly as py
#import plotly.graph_objs as go

#removes papers without authors
def soFreshAndSoCleanClean(Papers):
	for pid, paper in Papers.items():
		if len(paper.authors) < 1 or paper.path == '':
			del Papers[pid]
	return Papers
#assign N attributes to the data
def assignAttributes(Papers, PAA, N):
        data = {}
        index = 0
	scatterX = []
	scatterY = []
        #Year of Proceeding
        if (1 in N):
 #               print('assinging year of proceeding')
                for key, paper in Papers.items():
                        if paper.pid not in data:
                                data[paper.pid] = []
                        data[paper.pid].append(int(paper.year))
			scatterX.append(int(paper.year))
                index += 1
        #If 'vector machine' is a keyword of the paper (weight 10)
        if (2 in N):
 #               print('assining vector machine')
                checked = set()
                for key, paper in Papers.items():
                        if paper.pid not in data:
                                data[paper.pid] = []
                        data[paper.pid].append(0)
                        for keyword in paper.keywords:
                                if 'world wide web' in keyword:
                                        data[paper.pid][index] = 20
                index += 1
        #If 'vector machine' is a keyword of the paper (weight 10)
        if (3 in N):
 #               print('assining vector machine')
                checked = set()
                for key, paper in Papers.items():
                        if paper.pid not in data:
                                data[paper.pid] = []
                        data[paper.pid].append(0)
                        for keyword in paper.keywords:
                                if 'web search engine' in keyword:
                                        data[paper.pid][index] = 20
                index += 1
        #If 'vector machine' is a keyword of the paper (weight 10)
        if (4 in N):
 #               print('assining vector machine')
                checked = set()
                for key, paper in Papers.items():
                        if paper.pid not in data:
                                data[paper.pid] = []
                        data[paper.pid].append(0)
                        for keyword in paper.keywords:
                                if 'data mining' in keyword:
                                        data[paper.pid][index] = 20
                index += 1


        #Number of Authors who wrote the paper
        if (5 in N):
#                print('assinging author count')
                checked = set()
                for paper in PAA:
			if paper.pid not in Papers:
				continue
                        if paper.pid not in data:
                                data[paper.pid] = []
                        if paper.pid not in checked:
                                data[paper.pid].append(0)
                                checked.add(paper.pid)
                        data[paper.pid][index] += 1
		for pid in data.keys():
			scatterY.append(data[pid][index])
                index += 1

        #make scatter plot of num authors vs year written
#       if (1 in N and 2 in N):
#               trace = go.Scatter(
#                       x = scatterX,
#                       y = scatterY,
#                       mode = 'markers'
#               )
#               points = [trace]
#               py.iplot(points, filename='basic-scatter')

	return data




#gives some statistics on the dataset
def spicyStats(Papers):
	count = 0.0
	title = ''
	keywords = {}
	years = set()
	for pid, paper in Papers.items():
		years.add(paper.year)
		count += len(paper.authors)
		if len(paper.title) > len(title):
			title = paper.title
		for key in paper.keywords:
			if key in keywords:
				keywords[key] += 1
			else:
				keywords[key] = 0

	print('====Data Statistics====')
	print ('average number of authors per paper: ' + str(count/float(len(Papers.keys()))))
	print ('longest title: ' + str(len(title)) + ' characters')
	print ('most frequent keyword: ' + str(max(keywords.iteritems(), key=operator.itemgetter(1))[0]))
	print ('number of papers: ' + str(len(Papers.keys())))
	print('unique years: ' + str(len(years)))
	print('=======================')
