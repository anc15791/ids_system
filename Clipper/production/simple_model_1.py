
# coding: utf-8

# In[18]:


import logging, xgboost as xgb, numpy as np
from clipper_admin import ClipperConnection, DockerContainerManager
import pickle
from numpy import array
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import requests, json
from sklearn.ensemble import RandomForestClassifier

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


with open('../models/model.pickle', 'rb') as handle:
    model = pickle.load(handle)


# In[42]:



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
                                      version=3,
                                      input_type="floats",
                                      pkgs_to_install=['sklearn'],
                                      func=predict)


# In[44]:

try:
    clipper_conn.link_model_to_app('simple_model', 'simple-model')
except ClipperException as e:
    print(e)
