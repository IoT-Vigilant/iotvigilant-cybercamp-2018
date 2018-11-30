#!/usr/bin/python3
"""
###########################################
# IoT Vigilant Orchestrator
###########################################

--> Retrieves sniffed data from ElasticSearch
--> This data comes as simple FreeFlow data for each MAC associated device
--> Calls Anomalyzer to determine if the last temporal frame is an anomaly
--> Saves FreeFlow data for each MAC on the Database.
--> Every now and then,calls Modelizer to model the recent behaviour
of each MAC
--> Keeps track of the characteristics (GMM) for each MAC
"""

## Imports

from sklearn import mixture
from modelizer import modeler

import sys
import time
import numpy as np

print(__doc__)

#######################################################
############ Query the database    ####################
#######################################################

def get_freeFlow_parse():
    freeflow =0
    # Get last 5 minutes of data from the packet
    # database and parse it into a freeflow format
    return freeflow, maclist
def get_freeFlow_processed(samples):
    freeflow =0
    # get last N freeflow rows from elasticsearch
    return freeflow, maclist

def push_freeFlow(maclist, freeflow):
    # Send data to Elasticsearch
    return

#######################################################
#################### Config  ##########################
#######################################################
# Every 50 data batches extracted from the database, refresh the GMM model
gmm_remodel_period=125
gmm_model_size=250
# Every 5 min, extract data from the database and generate FreeFlow for each MAC
freeflow_time_size_seconds=5

def main_loop():
    ########## System Init
    # gmm_stack represents the current model for network behaviour
    # gmm_frames_old represents the number of times the model has
    # been used against new data
    ##########
    gmm_stack=[]
    gmm_frames_old=0
    freeflow_stack=[]

    # Get Data Processed samples from ElasticSearch
    freeflow_stack= get_freeFlow_processed(gmm_model_size)
    # Generate model
    if freeflow_stack!=[]:
    	gmm_stack = modeler(freeflow_stack)

    #######################################################
    ############ Core Detector Main loop ##################
    #######################################################
    while 1:
        # When GMM gets old, download lastest values and model 'em
        if gmm_frames_old > gmm_remodel_period:
            freeflow_stack= get_freeFlow_processed(gmm_model_size)
            gmm_stack= modeler(freeflow_stack)

        # Retrieves sniffed data from ElasticSearch EVERY 5 mins
        # Only last time frame

        freeflow_last= get_freeFlow_parse(1)
        ## TEST DATA
        freeflow_last= np.array([[0.68, -0.016,  4],[0.68, -0.016,  0.72]])

        # In case we already have acces to a GMM, calculate
        # posterior probabilities
        if gmm_stack!=[]:
            # Analyzes the posterior probability of each MAC against its GMM
            p_macs = gmm_stack.predict_proba(freeflow_last)
            ## Probability from each freeflow point to each Gaussian Component (rows are freeflow samples)
            print(p_macs)
            #freeflow_last.append(p_macs)
            gmm_frames_old +=1

        # Always, upload freeflow sample to populate database
        push_freeFlow(freeflow_last)


        # Do this every N min, to wait the sniffer to get some juicy packets
        print("waiting")
        time.sleep(freeflow_time_size_seconds)


##
# Looping code by https://stackoverflow.com/questions/8685695/how-do-i-run-long-term-infinite-python-processes
##
if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)


