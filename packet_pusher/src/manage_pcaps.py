'''
Read the schema from each schema file.
Download files and extract pcaps if necessary.
Move pcaps to /pcaps folder
take a number as input
    0 => download all files and extract pcaps
    +ve number => download only these many files.
'''
from zipfile import ZipFile
from os import walk, rename
import sys
import subprocess
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from utils import *
import urllib

schema_dir = "../schema/"
pcap_dir = "../pcaps/"
# unzip files for a given password
def unZip(file):
    try:
        with ZipFile(schema_dir+file) as zf:
            zf.extractall(pwd='infected666p',path=pcap_dir)
    except Exception as e:
        print(e)



# get filenames of contagio zip files
def getContagioZips():
    APT_PATH = "APT/"
    CRIME_PATH = "CRIME/"
    apt_pcaps =[]
    crime_pcaps =[]

    for (dirpath, dirnames, filenames) in walk(schema_dir+APT_PATH):
        apt_pcaps.extend(filenames)
        break
    for (dirpath, dirnames, filenames) in walk(schema_dir+CRIME_PATH):
        crime_pcaps.extend(filenames)
        break
    apt_pcaps = [APT_PATH + s for s in apt_pcaps]
    crime_pcaps = [CRIME_PATH + s for s in crime_pcaps]
    return apt_pcaps+crime_pcaps

# unzip files using threads.
def handleContagio(pcaps):
    pool = ThreadPool(4)
    try:
        results = pool.map(unZip,pcaps)
    except Exception as e:
        print(e)

#Download wrccdc files and move the pcaps to pcap directory
def downloadFiles(pcap_path):
    try:
        base_url = "https://archive.wrccdc.org/pcaps/2018/"
        urlib_opener = urllib.URLopener()
        urlib_opener.retrieve(base_url+pcap_path, pcap_path)
        rename(pcap_path, pcap_dir+pcap_path[4:-6]+".pcap")

    except Exception as e:
        print(e)

#create a thread pool to handle pcap dpwnloads
def handleWrccdc():

    wrccdc_list = readFile(schema_dir+"wrccdc.txt")
    pool = ThreadPool(6)
    try:
        results = pool.map(downloadFiles,wrccdc_list)
    except Exception as e:
        print(e)

def main():
    try:
        opt1 = sys.argv[1]
    except:
        print("invalid args: all|contagio|wrccdc")

    if opt1 == "contagio" or opt1 == "all":
        pcaps = getContagioZips()
        handleContagio(pcaps)
    if opt1 == "wrccdc" or opt1 == "all":
        handleWrccdc()



if __name__ == '__main__':
    main()
