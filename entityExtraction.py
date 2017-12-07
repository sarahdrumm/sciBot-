#!/usr/bin/python

def entityExtraction(Papers):
    paperid_path = []
    for pid, paper in Papers.items():
        paperid = paper.pid
        path = paper.path+'.txt'
        paperid_path.append([paperid,path])
    phrase2count = {}
    for [paperid,path] in paperid_path:
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
    fw = open('entities.txt','w')
    for [phrase,count] in sorted(phrase2count.items(),key=lambda x:-x[1]):
        fw.write(phrase+'\t'+str(count)+'\n')
    fw.close()

