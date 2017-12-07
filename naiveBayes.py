import os
import sys

class paper:
    def __init__(self, pid, title_case, title, year, conf, cid):
        self.pid = pid
        self.title_case = title_case
        self.title = title
        self.year = year
        self.conf = conf
        self.confs = set()
        self.keywords = set()
        self.authors = set()
        self.confs.add(conf)
        self.path = ''

def naiveBayes(Papers, confs, attributes):
    confCounts = {}
    for c in confs:
        confCounts[c] = [0]*(len(attributes)+1)
    attributeCounts = [0]*len(attributes)
    for a in range(len(attributes)):
        attributeCounts[a] = 0
    for pid, papers in Papers.items():
        confCounts[papers.conf][0] += 1
        for a in range(len(attributes)):
            if attributes[a] in papers.keywords:
                confCounts[papers.conf][a+1] += 1
                attributeCounts[a] += 1

#calculations
    probs = [0]*len(attributes)
    lenP = float(len(Papers))
    pX = 1.0
    pConf = [0]*len(confs)
    pConfX = [0]*len(confs) #P(conf|x)
    
    for a in range(len(attributes)):
        probs[a] = attributeCounts[a]/lenP
        pX *= probs[a]
    for c in range(len(confs)):
        pConf[c] = confCounts[confs[c]][0] / lenP
        pXConf = 1.0
        for a in range(len(attributes)):
            pXConf *= (float(confCounts[confs[c]][a+1]) / confCounts[confs[c]][0])
        inConf = confCounts[confs[c]][0] / lenP
        pConfX[c] = pXConf * pConf[c] / pX #inConf / pX
    maxVal = 0
    index = 0
    for c in range(len(confs)):
        if pConfX[c] > maxVal:
            maxVal = pConfX[c]
            index = c
    print('Given these attributes: ')
    for a in attributes:
        print('\t'+a)
    print(' a paper is most likely to be from the ' + str(confs[index]) + ' conference.' )



temp = '''Papers = {}
Papers['0'] = paper('1','YOLO', 'yolo', '2009', 'www', '123')
Papers['1'] = paper('2','ML',  'ml', '2011', 'kdd', '111')
Papers['0'].keywords.add('test1')
Papers['0'].keywords.add('test2')
Papers['0'].keywords.add('test3')
Papers['1'].keywords.add('test1')
Papers['1'].keywords.add('test4')
Papers['1'].keywords.add('test5')

naiveBayes(Papers, ['www', 'kdd'], ['test1', 'test2', 'test3' ])
'''
