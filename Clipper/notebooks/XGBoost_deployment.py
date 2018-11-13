
# coding: utf-8

# In[ ]:


import logging, xgboost as xgb, numpy as np
from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())


# In[ ]:


try:
    clipper_conn.start_clipper()
except:
    print("Clipper already running")
    clipper_conn.connect()


# In[ ]:


# We will register it to deploy an xgboost model.
clipper_conn.register_application('xgboost-test', 'integers', 'default_pred', 100000)


# In[ ]:


def get_test_point():
    return [np.random.randint(255) for _ in range(784)]


# In[ ]:


# Create a training matrix.
dtrain = xgb.DMatrix(get_test_point(), label=[0])
# We then create parameters, watchlist, and specify the number of rounds
# This is code that we use to build our XGBoost Model, and your code may differ.
param = {'max_depth': 2, 'eta': 1, 'silent': 1, 'objective': 'binary:logistic'}
watchlist = [(dtrain, 'train')]
num_round = 2
bst = xgb.train(param, dtrain, num_round, watchlist)


# In[ ]:


def predict(xs):
    return bst.predict(xgb.DMatrix(xs))


# In[ ]:


from clipper_admin.deployers import python as python_deployer
# We specify which packages to install in the pkgs_to_install arg.
# For example, if we wanted to install xgboost and psycopg2, we would use
# pkgs_to_install = ['xgboost', 'psycopg2']
python_deployer.deploy_python_closure(clipper_conn, name='xgboost-model', version=1,
     input_type="integers", func=predict, pkgs_to_install=['xgboost'])


# In[ ]:


clipper_conn.link_model_to_app('xgboost-test', 'xgboost-model')


# In[ ]:


import requests, json
# Get Address
addr = clipper_conn.get_query_addr()
# Post Query
response = requests.post(
     "http://%s/%s/predict" % (addr, 'xgboost-test'),
     headers={"Content-type": "application/json"},
     data=json.dumps({
         'input': get_test_point()
     }))
result = response.json()
if response.status_code == requests.codes.ok and result["default"]:
    print('A default prediction was returned.')
elif response.status_code != requests.codes.ok:
    print(result)
    raise BenchmarkException(response.text)
else:
    print('Prediction Returned:', result)


# In[ ]:


clipper_conn.stop_all()

