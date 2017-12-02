
# coding: utf-8

# In[1]:


from sklearn.cluster import KMeans
import numpy as np

X = np.array([[3,5], [3,4], [2,8], [2,3], [6,2], [6,4], [7,3], [7,4], [8,5], [7,6]])

kmeans = KMeans(n_clusters=2, random_state=0).fit(X)


# In[2]:


print kmeans.labels_


# In[3]:


print kmeans.cluster_centers_

