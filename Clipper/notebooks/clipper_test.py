
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import matplotlib.pyplot as plt 
import itertools
import numpy as np

from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# import some data to play with
iris = datasets.load_iris()
X = iris.data
y = iris.target
class_names = iris.target_names

# Split the data into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Run classifier, using a model that is too regularized (C too low) to see
# the impact on the results
classifier = svm.SVC(kernel='linear', C=0.1)
y_pred = classifier.fit(X_train, y_train).predict(X_test)


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# Compute confusion matrix
cnf_matrix = confusion_matrix(y_test, y_pred)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names,
                      title='Confusion matrix, without normalization')

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title='Normalized confusion matrix')

plt.show()


# In[ ]:



class_names[classifier.predict([[4.0, 2.0,1.0, 0.1]])][0]


# In[ ]:


class_names[classifier.predict([[7.9, 4.4,6.9, 2.5]])][0]


# In[ ]:


class_names[classifier.predict([[5.84, 3.05,3.76, 1.2]])]


# In[ ]:


class_names[classifier.predict([[5.84, 3.05,3.76, 1.2]])]


# In[ ]:


from clipper_admin import ClipperConnection, DockerContainerManager


# In[ ]:



clipper_conn = ClipperConnection(DockerContainerManager())


# In[ ]:


try:
    clipper_conn.start_clipper()
except:
    print("Clipper already running")
    clipper_conn.connect()


# In[ ]:


# Register an application called "hello_world". This will create
# a prediction REST endpoint at http://localhost:1337/hello_world/predict
clipper_conn.register_application(name="hello-world", 
                                  input_type="doubles", 
                                  default_output="-1.0", 
                                  slo_micros=100000)


# In[ ]:


# Register an application called "hello_world". This will create
# a prediction REST endpoint at http://localhost:1337/hello_world/predict

clipper_conn.register_application(name="iris", 
                                  input_type="doubles", 
                                  default_output="-1.0", 
                                  slo_micros=1000000000)

# Inspect Clipper to see the registered apps


# In[ ]:


clipper_conn.get_all_apps()


# In[ ]:



# Define a simple model that just returns the sum of each feature vector.
# Note that the prediction function takes a list of feature vectors as
# input and returns a list of strings.
def feature_sum(xs):
    return [str(sum(x)) for x in xs]


# In[ ]:


import sys  
import time 
import numpy as np
from sklearn import svm, datasets
iris = datasets.load_iris()
class_names = iris.target_names
def iris_predict(xs):
    #np.savetxt(sys.stdout.buffer, xs)
    pred = classifier.predict(xs)
    class_n = class_names[pred]
    ret = class_n[0]
    #np.savetxt(sys.stdout.buffer, ret)
    print(pred)
    print(class_n)
    print(ret)
    return pred


# In[ ]:


from clipper_admin.deployers import python as python_deployer


# In[ ]:



# Deploy the "feature_sum" function as a model. Notice that the application and model
# must have the same input type.
python_deployer.deploy_python_closure(clipper_conn, 
                                      name="sum-model", 
                                      version=1, 
                                      input_type="doubles", 
                                      func=feature_sum)


# In[ ]:



# Deploy the "iris_predict" function as a model. Notice that the application and model
# must have the same input type.
python_deployer.deploy_python_closure(clipper_conn, 
                                      name="iris-model", 
                                      version=1, 
                                      input_type="doubles", 
                                      func=iris_predict,
                                      pkgs_to_install=['numpy','scipy', 'scikit-learn'])


# In[ ]:


# Tell Clipper to route requests for the "hello-world" application to the "sum-model"
clipper_conn.link_model_to_app(app_name="hello-world", model_name="sum-model")


# In[ ]:


# Tell Clipper to route requests for the "iris" application to the "iris-model"
clipper_conn.link_model_to_app(app_name="iris", model_name="iris-model")

# Your iris application is now ready to serve predictions


# In[ ]:


clipper_conn.get_clipper_logs()


# In[ ]:


clipper_conn.cm.get_num_replicas(name="iris-model", version='1')


# In[ ]:


clipper_conn.get_linked_models(app_name="iris")


# In[ ]:


clipper_conn.cm.get_num_replicas(name="iris-model", version="8")


# In[ ]:


q1 = [4.3, 2.0,1.0, 0.1]
q2 = [5.84, 3.05,3.76, 1.2]
q3 = [7.9, 4.4, 6.9, 2.5]


# In[ ]:


import requests, json, numpy as np
headers = {"Content-type": "application/json"}


# In[ ]:


requests.post("http://localhost:1337/hello-world/predict", 
              headers=headers, 
              data=json.dumps({"input": q1})).json()


# In[ ]:



res = requests.post("http://localhost:1337/iris/predict", 
              headers=headers, 
              data=json.dumps({"input": q2})).json()
print(res)
[class_names[res['output']]]


# In[ ]:


res =requests.post("http://localhost:1337/iris/predict", 
              headers=headers, 
              data=json.dumps({"input": q3})).json()
print(res)
[class_names[res['output']]]


# In[ ]:



# you would change the hostname here if you were on a server or AWS :)
res =requests.post("http://127.0.0.1:1337/iris/predict", 
              headers=headers, 
              data=json.dumps({"input": q3})).json()
print(res)
[class_names[res['output']]]


# In[ ]:


res =requests.post("http://localhost:1337/iris/predict", 
              headers=headers, 
              data=json.dumps({"input": q2})).json()
print(res)
[class_names[res['output']]]


# In[ ]:


clipper_conn.stop_all()


# In[ ]:


clipper_conn.inspect_instance()

