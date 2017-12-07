#!/usr/bin/python

def entityTyping(Papers):
    n_type = 4
    s_method = 'method algorithm model approach framework process scheme implementation procedure strategy architecture'
    s_problem = 'problem technique process system application task evaluation tool paradigm benchmark software'
    s_dataset = 'data dataset database'
    s_metric = 'value score measure metric function parameter'
    types = ['METHOD','PROBLEM','DATASET','METRIC']
    wordsets = [set(s_method.split(' ')),set(s_problem.split(' ')),set(s_dataset.split(' ')),set(s_metric.split(' '))]

    paperid_path = []
    for pid, paper in Papers.items():
        paperid = paper.pid
        path = paper.path+'.txt'
        paperid_path.append([paperid,path])
    
    index,nindex = [{}],1 # phrase's index
    
    #phrases to parse files for
    fr = open('entities.txt','rb')
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

    # "__ __ __ __ __ support vector machine __ __ __ __ __"
    n_context = 5
    phrase2classifiers = {}
    for [paperid,path] in paperid_path:
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
                        if not phrase in phrase2classifiers:
                            phrase2classifiers[phrase] = [0,[[0 for t in range(0,n_type)] for c in range(0,n_context)]]
                        phrase2classifiers[phrase][0] += 1
                        for c in range(0,n_context):
                            if i-1-c >= 0:
                                trigger = wordslower[i-1-c]
                                for t in range(0,n_type):
                                    if trigger in wordsets[t]:
                                        phrase2classifiers[phrase][1][c][t] += 1
#										for _c in range(c,n_context):
#											phrase2classifiers[phrase][1][_c][t] += 1
                            if i+k+c < l:
                                trigger = wordslower[i+k+c]
                                for t in range(0,n_type):
                                    if trigger in wordsets[t]:
                                        phrase2classifiers[phrase][1][c][t] += 1
#										for _c in range(c,n_context):
#											phrase2classifiers[phrase][1][_c][t] += 1
                        isvalid = True
                        break
                if isvalid:
                    i += j
                    continue
                i += 1
        fr.close()
    fw = open('entityTyping.txt','w')
    s = 'ENTITY\tCOUNT'
    for c in range(0,n_context): s += '\tWINDOWSIZE'+str(c+1)
    fw.write(s+'\n')
    for [phrase,[count,ctmatrix]] in sorted(phrase2classifiers.items(),key=lambda x:-x[1][0]):
        s = phrase+'\t'+str(count)
        for c in range(0,n_context):
            maxv,maxt = -1,-1
            for t in range(0,n_type):
                v = ctmatrix[c][t]
                if v > maxv:
                    maxv = v
                    maxt = t
            if maxv == 0:
                s += '\tN/A'
            else:
                s += '\t'+types[maxt]
                for t in range(0,n_type):
                    v = ctmatrix[c][t]
                    if v == 0: continue
                    s += ' '+types[t][0]+types[t][-1]+':'+str(v)
        fw.write(s+'\n')
    fw.close()


