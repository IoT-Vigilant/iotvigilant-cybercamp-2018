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
from modelizer import modeler,model_By_Mac
from esconector import *

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

    metrics = get_metrics(freeflow_time_size_min)

    ## TEST DATA ## Results of parsing should be like these
    maclist = metrics[0] # ["0A:03:32:AD:32:41", "0A:03:32:AD:32:42", "0A:03:32:AD:32:43"]
    freeflow = np.array(metrics[1:]).T # np.array([[0.68, -0.016,  4],[0.68, -0.016,  0.72], [0.61, -0.013,  0.74]])
    
    return maclist, freeflow

def get_freeFlow_processed(samples):
    freeflow_list=[]
    maclist_list=[]
    # get last N freeflow rows from elasticsearch

    ## TEST DATA ## Results of parsing should be like these
    '''
    for i in range(samples):
        freeflow_list.append(np.array([[0.68, -0.016,  4], [0.5, -0.5,  0.92], [0.21, -0.13,  0.31]]))
        maclist_list.append(["0A:03:32:AD:32:41", "0A:03:32:AD:32:42", "0A:03:32:AD:32:43"])
    '''

    result = get_bulk_pro_data(samples)

    maclist_list = result[0]
    freeflow_list = np.array(result[1:]).T

    return maclist_list, freeflow_list


def push_freeFlow(maclist, freeflow, prob_list=[]):
    # Send data to Elasticsearch
    load_data(maclist,freeflow,prob_list)


#######################################################
####### Posterior probability calculation #############
#######################################################
## This script associates macs with freeflow vectors
## in order to collect correct probabilities for each mac


def GMM_Probability_Pairs_calculator(maclist_last, freeflow_last, gmm_stack, mac_gmm_stack):
    p_list=[]
    p_list_macs=[]
    for index, mac in enumerate(maclist_last):
        if mac in mac_gmm_stack:
            # Calculate predict_prob for each pair mac -> freeflow row
        
            print(freeflow_last[index,:])
            post_proba=gmm_stack[index].predict_proba(freeflow_last[index,:].reshape(1, -1))
            

            p_list.append(np.amax(post_proba))
            p_list_macs.append(mac)
    return p_list, p_list_macs



#######################################################
#################### Config  ##########################
#######################################################
# Every 50 data batches extracted from the database, refresh the GMM model
gmm_remodel_period=10
gmm_model_size=400
# Every 5 min, extract data from the database and generate FreeFlow for each MAC
freeflow_time_size_min=1



def main_loop():

    gmm_frames_old=0
    ########## System Init
    # gmm_stack represents the current model for network behaviour
    # gmm_frames_old represents the number of times the model has
    # been used against new data
    ##########

    gmm_stack=[]
    freeflow_stack=[]

    # Get Data Processed samples from ElasticSearch
    maclist_stack, freeflow_stack= get_freeFlow_processed(gmm_model_size)

    # Generate model
    #if len(freeflow_stack)>=gmm_model_size:
    print("CREATING GMM WITH")
    print(maclist_stack)
    print(freeflow_stack)
    gmm_stack, mac_gmm_stack = model_By_Mac(maclist_stack, freeflow_stack)

    #######################################################
    ############ Core Detector Main loop ##################
    #######################################################
    while 1:
        # When GMM gets old, download lastest values and model 'em
        print("Samples Analyzed")
        print(gmm_frames_old)
        if gmm_frames_old >= gmm_remodel_period:
            print("CREATING GMM")
            maclist_stack, freeflow_stack= get_freeFlow_processed(gmm_model_size)
            gmm_stack, mac_gmm_stack= model_By_Mac(maclist_stack, freeflow_stack)
            gmm_frames_old =0
        # Retrieves sniffed data from ElasticSearch every "freeflow_time_size_seconds"
        # Only last time frame

        maclist_last, freeflow_last= get_freeFlow_parse()


        # In case we already have acces to a GMM, calculate
        # posterior probabilities
        if gmm_stack!=[]:
            # Macs anomaly probability values
            prob_value_macs = []
            # Related mac names (1 to 1 with previous)
            prob_name_macs = []

            freeflow_values=[]

            freeflow_last_probs = [None] * len(maclist_last)
            print("Waiting for new data to analyze")
            # Analyzes the posterior probability of each MAC against its GMM
            ## Probability from each freeflow point to each Gaussian Component (rows are freeflow samples)
            # Do this every N min, to wait the sniffer to get some juicy packets
            print("waiting")
            time.sleep(freeflow_time_size_min*15+20)
            prob_value_macs, prob_name_macs = GMM_Probability_Pairs_calculator(maclist_last, freeflow_last, gmm_stack, mac_gmm_stack)

            #freeflow_last.append(p_macs)
            print("Macs analizadas")             
            print(prob_name_macs)
            print("Probabilidad de dato normal") 
            print(prob_value_macs)


            #### ONLY push data with prob values
            ### Calculate indexes with prob data


            if  prob_name_macs:

                for name_mac in prob_name_macs:
                    print("MAC EQUALS "+name_mac)
                    freeflow_prob_index = [index for index, value in enumerate(maclist_last) if value == name_mac]
                    print("FOUND INDEXES "+str(freeflow_prob_index))
                    for freeflow_index in freeflow_prob_index:
                        print("APPENDING VALUE "+str(freeflow_last[freeflow_index,:]))
                        freeflow_values.append(freeflow_last[freeflow_index,:])



            #         freeflow_prob_index = [index for index, value in enumerate(maclist_last) if value == aux]
            #         for aux2 in freeflow_prob_index:
            #             aux3.append(freeflow_last[aux2])
            #     empty_list=[]
            #     for index,el in enumerate(aux3[0]):
            #         empty_list.append(int(el))
                # print("MAC NAMES "+str(prob_name_macs))
                # print("MAC VALUES "+str(freeflow_values))
                # print("MAC PROBS "+str(prob_value_macs))


                push_freeFlow(prob_name_macs, freeflow_values ,prob_value_macs)
                gmm_frames_old +=1

        # Always, upload freeflow sample to populate database
        push_freeFlow(maclist_last, freeflow_last)



##
# Looping code by https://stackoverflow.com/questions/8685695/how-do-i-run-long-term-infinite-python-processes
##
if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)


