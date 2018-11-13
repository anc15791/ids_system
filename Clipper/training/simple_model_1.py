
# coding: utf-8
import pickle
from numpy import array
import numpy as np
from sklearn.ensemble import RandomForestClassifier

#importint the libraries
import numpy as np
import pandas as pd
import csv
import os.path


dataset = pd.read_csv('../dataset/input.csv', sep="\t", header=None)
dataset.columns = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X"]
X= dataset[['C','D','E','F','G','H','I','J','K','L','M',"P"]]
df=pd.DataFrame(X)
Y=dataset['R']



from sklearn.model_selection  import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(df, Y, test_size =0.3, random_state=0)


# In[22]:


clf = RandomForestClassifier(n_estimators=100, max_depth=2,random_state=0 )
clf.fit(X_train, Y_train)


# In[23]:


with open('../models/model.pickle', 'wb') as handle:
    pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)
