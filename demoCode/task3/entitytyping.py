#!/usr/bin/python

def SimpleEntityExtraction():
	paperid_path = []
	fr = open('microsoft/index.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split('\t')
		paperid = arr[2]
		path = 'text/'+arr[0]+'/'+arr[1]+'.txt'
		paperid_path.append([paperid,path])
	fr.close()
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
	fw = open('phrase2count.txt','w')
	for [phrase,count] in sorted(phrase2count.items(),key=lambda x:-x[1]):
		fw.write(phrase+'\t'+str(count)+'\n')
	fw.close()

def SimpleEntityTyping():
	n_type = 4
	s_method = 'method algorithm model approach framework process scheme implementation procedure strategy architecture'
	s_problem = 'problem technique process system application task evaluation tool paradigm benchmark software'
	s_dataset = 'data dataset database'
	s_metric = 'value score measure metric function parameter'
	types = ['METHOD','PROBLEM','DATASET','METRIC']
	wordsets = [set(s_method.split(' ')),set(s_problem.split(' ')),set(s_dataset.split(' ')),set(s_metric.split(' '))]

	paperid_path = []
	fr = open('microsoft/index.txt','rb')
	for line in fr:
		arr = line.strip('\r\n').split('\t')
		paperid = arr[2]
		path = 'text/'+arr[0]+'/'+arr[1]+'.txt'
		paperid_path.append([paperid,path])
	fr.close()
	index,nindex = [{}],1 # phrase's index
	fr = open('phrase2count.txt','rb')
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
	fw = open('entitytyping.txt','w')
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

#SimpleEntityExtraction()
SimpleEntityTyping()

