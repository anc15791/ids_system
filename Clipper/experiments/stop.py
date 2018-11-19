import sys
import os
pathlist = ['/home/sdn-nfv/Desktop/ids_system/Clipper/experiments', '/home/sdn-nfv/anaconda3/envs/py35/lib/python35.zip',
'/home/sdn-nfv/anaconda3/envs/py35/lib/python3.5', '/home/sdn-nfv/anaconda3/envs/py35/lib/python3.5/plat-linux',
'/home/sdn-nfv/anaconda3/envs/py35/lib/python3.5/lib-dynload', '/home/sdn-nfv/.local/lib/python3.5/site-packages',
'/home/sdn-nfv/anaconda3/envs/py35/lib/python3.5/site-packages',"/home/sdn-nfv/Desktop/clipper/clipper_admin/clipper_admin/",
'/home/sdn-nfv/anaconda3/envs/py35/lib/python3.5/site-packages/ksql-0.5.1-py3.5.egg', "/home/sdn-nfv/Desktop/clipper",
"/home/sdn-nfv/Desktop/clipper/clipper_admin"]

os.environ["PATH"] = os.pathsep.join(pathlist) + os.environ["PATH"]


from clipper_admin import ClipperConnection, DockerContainerManager
clipper_conn = ClipperConnection(DockerContainerManager())

try:
    clipper_conn.start_clipper()
except:
    print("Clipper already running")
    clipper_conn.connect()

if(clipper_conn):
    print("stop clipper")
    clipper_conn.stop_all()
else:
    print("no clipper connection")
