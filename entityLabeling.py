#!/usr/bin/python

import re

def entityLabeling():
    fr = open('entityTyping.txt','rb')
    
    problems = []
    methods = []
    datasets = []
    metrics = []

    for line in fr:
        arr = line.strip('\r\n').split('\t')
        count = [0, 0, 0, 0] 
        typed = ["PROBLEM", "METHOD", "DATASET", "METRIC"]
        for val in arr:
            if val.startswith("PROBLEM"):
                count[0] += 1
            if val.startswith("METHOD"):
                count[1] += 1
            if val.startswith("DATASET"):
                count[2] += 1
            if val.startswith("METRIC"):
                count[3] += 1
        it = -1
        for c in count:
            it += 1
            if c >= 3:
                if it == 0:
                    problems.append(arr[0])
                if it == 1:
                    methods.append(arr[0])
                if it == 2:
                    datasets.append(arr[0])
                if it == 3:
                    metrics.append(arr[0])
                
    fr.close()

    fw = open('problem.txt', 'w')
    for line in problems:
        fw.write(line+'\n')
    fw.close()

    fw = open('method.txt', 'w')
    for line in methods:
        fw.write(line+'\n')
    fw.close()

    fw = open('dataset.txt', 'w')
    for line in datasets:
        fw.write(line+'\n')
    fw.close()

    fw = open('metric.txt', 'w')
    for line in metrics:
        fw.write(line+'\n')
    fw.close()

entityLabeling()


