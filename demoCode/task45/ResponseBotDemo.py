
# coding: utf-8

# In[1]:


def easy_tokenizer(text):
	ret = []
	for x in [',','.','--','!','?',';','(',')','/','"']:
		text = text.replace(x,' '+x+' ')
	for word in text.split(' '):
		if word == '': continue
		ret.append(word.lower())
	return ret

responses = []
fr = open('response.txt','rb')
for line in fr:
	text = line.strip('\r\n') # "Class is not valuable."
	words = easy_tokenizer(text) # ['class','is','not','valuable','.']
	responses.append(words)
fr.close()
# output
for words in responses: print words


# In[2]:


stopwordset = set()
fr = open('stopwords.txt','rb')
for line in fr:
	word = line.strip('\r\n').lower()
	stopwordset.add(word)
fr.close()
stopwordset.add('class')

word2support = {}
for words in responses:
	for word in set(words):
		if word in stopwordset or len(word) == 1 or word.isdigit(): continue
		if not word in word2support:
			word2support[word] = 0
		word2support[word] += 1
# output
for [word,support] in sorted(word2support.items(),key=lambda x:-x[1]):
	if support == 1: break
	print word,support


# In[3]:


word2count = {}
for words in responses:
	for word in words:
		if word in stopwordset or len(word) == 1 or word.isdigit(): continue
		if not word in word2count:
			word2count[word] = 0
		word2count[word] += 1
bigram2score = {} # bigram's count, first word's count, second word's count, significance score
L = 0
for words in responses:
	n = len(words)
	L += n
	for i in range(0,n-1):
		if words[i] in word2count and words[i+1] in word2count:
			bigram = words[i]+'_'+words[i+1]
			if not bigram in bigram2score:
				bigram2score[bigram] = [0,word2count[words[i]],word2count[words[i+1]],0.0]
			bigram2score[bigram][0] += 1
for bigram in bigram2score:
	bigram2score[bigram][3] = (1.0*bigram2score[bigram][0] -  		1.0*bigram2score[bigram][1]*bigram2score[bigram][2]/L) / 		( (1.0*bigram2score[bigram][0])**0.5 )
# output
print 'bigram','count-bigram','count-first-word','count-second-word','significance-score'
for [bigram,score] in sorted(bigram2score.items(),key=lambda x:-x[1][3]):
	print bigram,score[0],score[1],score[2],score[3]


# In[4]:


bigramdict = {}
for bigram in bigram2score:
	if bigram2score[bigram][0] > 1:
		[firstword,secondword] = bigram.split('_')
		if not firstword in bigramdict:
			bigramdict[firstword] = set()
		bigramdict[firstword].add(secondword)

transactions = [] # response
for words in responses:
	transaction = set() # set of words/bigrams
	n = len(words)
	i = 0
	while i < n:
		if words[i] in bigramdict and i+1 < n and words[i+1] in bigramdict[words[i]]:
			transaction.add(words[i]+'_'+words[i+1])
			i += 2
			continue
		if words[i] in stopwordset or len(words[i]) == 1 or words[i].isdigit():
			i += 1
			continue
		transaction.add(words[i])
		i += 1
	transactions.append(list(transaction))
# output
for transaction in transactions:
	print transaction


# In[5]:


# http://www.borgelt.net/pyfim.html	
from fim import apriori, fpgrowth
patterns = apriori(transactions,supp=-3) # +: percentage -: absolute number
# output
print '-------- Apriori --------'
for (pattern,support) in sorted(patterns,key=lambda x:-x[1]):
	print pattern,support
print 'Number of patterns:',len(patterns)


# In[6]:


patterns = fpgrowth(transactions,supp=-3)
# output
print '-------- FP-Growth --------'
for (pattern,support) in sorted(patterns,key=lambda x:-x[1]):
	print pattern,support
print 'Number of patterns:',len(patterns)


# In[7]:


patterns = fpgrowth(transactions,target='c',supp=-2,zmin=2)
# output
print '-------- Closed Non-single Itemsets --------'
for (pattern,support) in sorted(patterns,key=lambda x:-x[1]):
	print pattern,support
print 'Number of patterns:',len(patterns)


# In[8]:


rules = apriori(transactions,target='r',supp=-2,conf=70,report='sc')
# output
print '-------- One-to-Many Association Rules --------'
for (ruleleft,ruleright,support,confidence) in sorted(rules,key=lambda x:x[0]):
	print ruleleft,'-->',ruleright,support,confidence
print 'Number of rules:',len(rules)

