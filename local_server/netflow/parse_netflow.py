#!/usr/bin/python3

import sys, os, subprocess, csv, json
from elasticsearch import Elasticsearch

#Elasticsearch variables
es_host = "localhost"
es_port = 9200
es_index = "rawdata"
es_doc_type = "ts"

folderPath = sys.argv[1]
cont = 0

def config_params():
	"""
	Configure the parameters used to connect to the Elasticsearch and the port where the server is going to listen
	"""
	global es_host, es_port

	if "IOTV_ES_HOST" in os.environ:
		es_host = os.getenv("IOTV_ES_HOST")
	if "IOTV_ES_PORT" in os.environ:
		es_port = int(os.getenv("IOTV_ES_PORT"))


def csv_to_es(csvPath):
    """
    It retrieves all the important parameters from the csv and saves the into elasticsearch
    """
    with open(csvPath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            new_obj = {"MacOrigen": row["ismc"], 
            "IpOrigen": row["sa"], 
            "IpDestino": row["da"], 
            "TCPseq": 0, 
            "PuertoOrigen": row["sp"], 
            "PuertoDestino": row["dp"], 
            "layers": row["pr"]}
            print(new_obj)
            
            es.index(index=es_index, doc_type=es_doc_type, body=json.dumps(new_obj))
    
    os.remove(csvPath)

def nfdump_wrapper(filename):
    """
    Call to nfdump to transform logs to csv and then, call to csv_to_dict
    """
    global folderPath, cont

    filePath = folderPath + "/" + filename
    if not len(filename) > 1 or not os.path.isfile(filePath):
        return
    
    newFile = folderPath+"/"+str(cont)+".csv"
    result = subprocess.run(['nfdump -R '+ filePath +' -o csv | head -n -4 > '+newFile], shell=True)
    os.remove(filePath)
    cont += 1

    csv_to_es(newFile)


def logs_to_csv():
    """
    First function, it takes all the log files and transform them into csv using nfdump
    """
    global folderPath

    f=[]
    for (dirpath, dirname, filename) in os.walk(folderPath):
        f.extend(filename)

    for filename in f:
        if (not "current" in filename) and ("nfcapd" in filename):
            nfdump_wrapper(filename)


if __name__ == "__main__":
    config_params()
    logs_to_csv()