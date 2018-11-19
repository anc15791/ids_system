import sys
import os

pathlist = ['/home/sdn-nfv/Desktop/ids_system/Clipper/experiments', '/home/sdn-nfv/anaconda3/envs/py35/lib/python35.zip',
'/home/sdn-nfv/anaconda3/envs/py35/lib/python3.5', '/home/sdn-nfv/anaconda3/envs/py35/lib/python3.5/plat-linux',
'/home/sdn-nfv/anaconda3/envs/py35/lib/python3.5/lib-dynload', '/home/sdn-nfv/.local/lib/python3.5/site-packages',
'/home/sdn-nfv/anaconda3/envs/py35/lib/python3.5/site-packages',"/home/sdn-nfv/Desktop/clipper/clipper_admin/clipper_admin/",
'/home/sdn-nfv/anaconda3/envs/py35/lib/python3.5/site-packages/ksql-0.5.1-py3.5.egg', "/home/sdn-nfv/Desktop/clipper",
"/home/sdn-nfv/Desktop/clipper/clipper_admin"]

os.environ["PATH"] = os.pathsep.join(pathlist) + os.environ["PATH"]

import logging
from clipper_admin import ClipperConnection, DockerContainerManager
from clipper_admin.exceptions import ClipperException
import pickle
from numpy import array
import numpy as np
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

try:
    clipper_conn.register_application(name='simple_model',
                                      input_type='floats',
                                      default_output="-1.0",
                                      slo_micros=100000)
except ClipperException as e:
    print(str(e))

# In[29]:


with open('model.pickle', 'rb') as handle:
    model = pickle.load(handle)


# In[42]:



def predict(xs):
    print("xs: ",xs)
    res= []
    for x in xs:
        x = x.reshape(1, -1)
        res.append(str(model.predict(x)))
    print("res: ", res)
    return res



# In[43]:


from clipper_admin.deployers import python as python_deployer
# We specify which packages to install in the pkgs_to_install arg.
# For example, if we wanted to install xgboost and psycopg2, we would use
# pkgs_to_install = ['xgboost', 'psycopg2']
python_deployer.deploy_python_closure(clipper_conn,
                                      name='simple-model',
                                      version=1,
                                      input_type="floats",
                                      pkgs_to_install=['sklearn'],
                                      func=predict)


# In[44]:

try:
    clipper_conn.link_model_to_app('simple_model', 'simple-model')
except ClipperException as e:
    print(e)

addr = clipper_conn.get_query_addr()
print(addr)
