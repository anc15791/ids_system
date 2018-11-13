
# coding: utf-8

# In[1]:


from kafka import KafkaConsumer,TopicPartition
import json
import ast
from kafka import KafkaProducer
from kafka.errors import KafkaError
import os
import sys
# In[2]:

if "EXP_NAME" in os.environ:
    EXP_NAME = os.environ["EXP_NAME"]
else:
    EXP_NAME = "anurag_test_1"


if "CONSUMER_BOOTSTRAP_SERVER" in os.environ:
    CONSUMER_BOOTSTRAP_SERVER = os.environ["CONSUMER_BOOTSTRAP_SERVER"]
else:
    CONSUMER_BOOTSTRAP_SERVER = None

if "PRODUCER_BOOTSTRAP_SERVER" in os.environ:
    PRODUCER_BOOTSTRAP_SERVER = os.environ["PRODUCER_BOOTSTRAP_SERVER"]
else:
    PRODUCER_BOOTSTRAP_SERVER = None

if "CONSUMER_CLIENT_ID" in os.environ:
    CONSUMER_CLIENT_ID = os.environ["CONSUMER_CLIENT_ID"]
else:
    CONSUMER_CLIENT_ID = "kafka_consumer_"+EXP_NAME

if "PRODUCER_CLIENT_ID" in os.environ:
    PRODUCER_CLIENT_ID = os.environ["PRODUCER_CLIENT_ID"]
else:
    PRODUCER_CLIENT_ID = "kafka_producer_"+EXP_NAME



if "AUTO_COMMIT_INTERVAL_MS" in os.environ:
    AUTO_COMMIT_INTERVAL_MS = int(os.environ["AUTO_COMMIT_INTERVAL_MS"])
else:
    AUTO_COMMIT_INTERVAL_MS = 1



if "CONSUMER_GROUP_ID" in os.environ:
    CONSUMER_GROUP_ID = os.environ["CONSUMER_GROUP_ID"]
else:
    CONSUMER_GROUP_ID = "no_group"


if "CONSUMER_TOPIC_NAME" in os.environ:
    CONSUMER_TOPIC_NAME = os.environ["CONSUMER_TOPIC_NAME"]
else:
    CONSUMER_TOPIC_NAME = None

if "PRODUCER_TOPIC_NAME" in os.environ:
    PRODUCER_TOPIC_NAME = os.environ["PRODUCER_TOPIC_NAME"]
else:
    PRODUCER_TOPIC_NAME = None




if CONSUMER_TOPIC_NAME is None:
    print("CONSUMER_TOPIC_NAME not provided")


if PRODUCER_TOPIC_NAME is None:
    print("PRODUCER_TOPIC_NAME not provided")
    sys.exit(-1)

if PRODUCER_BOOTSTRAP_SERVER is None:
    print("PRODUCER_BOOTSTRAP_SERVER not provided")
    sys.exit(-1)

if CONSUMER_BOOTSTRAP_SERVER is None:
    print("CONSUMER_BOOTSTRAP_SERVER not provided")
    sys.exit(-1)
# docker exec -u 0 kafka_kafka-1_1 kafka-consumer-groups --describe --group bro_conn_log --bootstrap-server localhost:19092


# In[3]:
print("in python start for ",EXP_NAME)

consumer = KafkaConsumer(
    CONSUMER_TOPIC_NAME,
    bootstrap_servers=CONSUMER_BOOTSTRAP_SERVER,
    client_id=CONSUMER_CLIENT_ID,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    auto_commit_interval_ms=AUTO_COMMIT_INTERVAL_MS,
    group_id=CONSUMER_GROUP_ID)

producer = KafkaProducer(
    bootstrap_servers=PRODUCER_BOOTSTRAP_SERVER,
    client_id=PRODUCER_CLIENT_ID,
    retries =1,
    linger_ms=5,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


# In[ ]:


till = 10
i=0
while(True):

    print("----------------------------------------------------------------------")
    msg = next(consumer)
    topic = msg.topic
    partition = msg.partition
    offset = msg.offset
    try:
        value = json.loads(msg.value.decode('utf-8'))
    except TypeError as e:
        print("Error in msg.value convertion to json\n", e)
        consumer.close()
    try:
        value['message'] = json.loads(value['message'])
    except:
        pass

    print("topic: ",topic)
    print("partition: ", partition)
    print("offset: ",offset)
    print(value)
    producer.send(PRODUCER_TOPIC_NAME,value)
    i+=1
    if i>till:
        consumer.close()
        break
