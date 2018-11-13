
# coding: utf-8

# In[18]:


import logging, xgboost as xgb, numpy as np
from clipper_admin import ClipperConnection, DockerContainerManager
import pickle
from numpy import array
import numpy as np
from sklearn.ensemble import RandomForestClassifier


# In[19]:


#importint the libraries
import numpy as np
import pandas as pd
import csv
import os.path


from sklearn.ensemble import RandomForestClassifier



# In[20]:


dataset = pd.read_csv('input.csv', sep="\t", header=None)
dataset.columns = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X"]
X= dataset[['C','D','E','F','G','H','I','J','K','L','M',"P"]]
df=pd.DataFrame(X)
Y=dataset['R']
df.dtypes


# In[21]:


from sklearn.model_selection  import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(df, Y, test_size =0.3, random_state=0)


# In[22]:


clf = RandomForestClassifier(n_estimators=100, max_depth=2,random_state=0 )          
clf.fit(X_train, Y_train)


# In[23]:


with open('model.pickle', 'wb') as handle:
    pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)


# In[24]:


clipper_conn = ClipperConnection(DockerContainerManager())


# In[25]:


FEATURE_SET="uid,history,connection_state_description,src_packets,src_bytes,dst_bytes,dIp,sIp,duration,dst_packets,sP,dP"
FEATURE_SET = FEATURE_SET.split(",")


# In[26]:


try:
    clipper_conn.start_clipper()
except:
    print("Clipper already running")
    clipper_conn.connect()


# In[28]:


# We will register it to deploy a simple model.
clipper_conn.register_application(name='simple_model', 
                                  input_type='floats', 
                                  default_output="-1.0", 
                                  slo_micros=100000)


# In[29]:


with open('model.pickle', 'rb') as handle:
    model = pickle.load(handle)


# In[42]:


from sklearn.ensemble import RandomForestClassifier
def predict(xs):
    print("xs: ",xs)
    res = model.predict(xs)
    print("res: ", res)
    return res
    


# In[43]:


from clipper_admin.deployers import python as python_deployer
# We specify which packages to install in the pkgs_to_install arg.
# For example, if we wanted to install xgboost and psycopg2, we would use
# pkgs_to_install = ['xgboost', 'psycopg2']
python_deployer.deploy_python_closure(clipper_conn, 
                                      name='simple-model', 
                                      version=2,
                                      input_type="floats", 
                                      pkgs_to_install=['sklearn'],
                                      func=predict)


# In[44]:


clipper_conn.link_model_to_app('simple_model', 'simple-model')


# In[47]:


import requests, json
# Get Address
addr = clipper_conn.get_query_addr()
# Post Query

data = [118586235192977525301275,12459745583622286062,158036878717837878020514440491555919575,2,0,0,245734465685311455698562072742206145221,258155230841023532689246593572124345694,1.1e-05,0,37593,39596]

data=np.array(data,float)
response = requests.post(
     "http://%s/%s/predict" % (addr, 'simple_model'),
     headers={"Content-type": "application/json"},
     data=json.dumps({
         'input': data.tolist()
     }))
result = response.json()
if response.status_code == requests.codes.ok and result["default"]:
    print('A default prediction was returned.')
elif response.status_code != requests.codes.ok:
    print(result)
    raise BenchmarkException(response.text)
else:
    print('Prediction Returned:', result)


# In[48]:


clipper_conn.stop_all()

