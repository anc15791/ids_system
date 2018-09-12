'''
This script will read pcap files from pcap_dir and replay them to the interface.
User can provide two options
    old = it skips over the seen files and only replays unseen files
    new = it will replay all files and remove the seen_ tag from each file.
Depending upong number of pcaps to replay, script can replay 4 at the same time using threads.
'''

from os import walk, rename
import sys
import subprocess
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


pcap_dir = "../pcaps/"
loop_count = "" # --loop=2
speed_flag = "" # --mbps=1
quiet_flag = "" # --quiet
interface = "en0"

def exec_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    #print(out)
    return out,err


def getUnseenFileList(dir,opt):
    f = []
    unseen_files = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(filenames)
        break
    for file_name in f:
        if opt == "new":
            new_pcap_file = file_name[5:]
            rename(pcap_dir+file_name, pcap_dir+new_pcap_file )
            unseen_files.append(new_pcap_file)
        if "seen" in file_name :
            pass #move file to archive
        else:
            unseen_files.append(file_name)

    return unseen_files

# replay pcap file on a given interface and rename them as seen_
def tcpReplay(pcap_file):
    print("replaying "+ pcap_file)
    int = ""


    if interface != None:
        int = '--intf1=' +interface
    else:
        raise Exception("interface not provided")

    if ".pcap" not in pcap_file:
        raise Exception("invalid pcap file")


    try:
        out, err = exec_command(["sudo","tcpreplay", int, pcap_dir+pcap_file])
        print(out)
        if err:
            raise Exception(err)
        else:
            rename(pcap_dir+pcap_file, pcap_dir+"seen_"+pcap_file )
    except Exception as e:
        raise e

def main():

    try:
        opt1 = sys.argv[1]
    except:
        print("invalid args")
        return

    print("options are " + opt1)

    if str(opt1) == "old" or str(opt1) == "new":
        pass
    else:
        print("first argument is old|new")
        return
    pool = ThreadPool(4)

    file_list = getUnseenFileList(pcap_dir, opt1)
    if not file_list:
        print("file list empty.")
        return

    print(file_list)


    try:
        results = pool.map(tcpReplay,file_list)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    main()
