#!/usr/bin/python3
"""
###########################################
# IoT Vigilant Orchestrator
###########################################
"""

from elasticsearch import Elasticsearch
import time

es_host = "localhost"
es_port = 9200
es_index = "rawdata"
es_index_ml = "mloutput"
es_doc_type = "ts"

es = Elasticsearch([{'host': es_host, 'port': es_port}])

def get_n_packets(interval):

	interval = 60000 * interval

	queryUniqueMacs = {
					   "query":{
					      "bool":{
					         "must":{
					            "range":{
					               "@timestamp":{
					                  "gte":int(round(time.time() * 1000)) - interval,
					                  # ini date
					                "lte":int(round(time.time() * 1000)),
					                  # end date
					                "format":"epoch_millis"
					               }
					            }
					         }
					      }
					   },
					   "aggs":{
					      "by_mac":{
					         "terms":{
					            "field":"MacOrigen"
					         }    
					            }
					         
					      }
					   }

	response = es.search(index = es_index, doc_type=es_doc_type, size='100', body = queryUniqueMacs)

	lista = response['aggregations']['by_mac']['buckets']

	result_macs = []

	results = []

	for l in lista:
		result_macs.append( str(l['key']))
		results.append(str(l['doc_count']))

	return [result_macs,results]

def get_metric_by_mac(interval,metric):

	interval = interval * 60000

	queryUniqueMacs = {
					   "query":{
					      "bool":{
					         "must":{
					            "range":{
					               "@timestamp":{
					                  "gte":int(round(time.time() * 1000)) - interval,
					                  # ini date
					                "lte":int(round(time.time() * 1000)),
					                  # end date
					                "format":"epoch_millis"
					               }
					            }
					         }
					      }
					   },
					   "aggs":{
					      "by_mac":{
					         "terms":{
					            "field":"MacOrigen"
					         },
					               "aggs":{
					                  "count_diff":{
					                     "cardinality":{
					                        "field":metric,
					                     },

					                     }
					                  }
					               }
					            }
					         
					      }
					   
					

	response = es.search(index = es_index, doc_type=es_doc_type, size='100', body = queryUniqueMacs)

	lista = response['aggregations']['by_mac']['buckets']

	result_macs = []

	results = []

	for l in lista:
		result_macs.append( str(l['key']))
		results.append(str(l['count_diff']['value']))

	return [result_macs,results]

def get_metrics(interval):
	
	macs = get_metric_by_mac(interval, "IpOrigen")[0]
	diff_srcips = get_metric_by_mac(interval, "IpOrigen")[1]
	diff_dstips = (get_metric_by_mac(interval, "IpDestino"))[1]
	diff_srcports = (get_metric_by_mac(interval, "PuertoOrigen"))[1]
	diff_dstports = (get_metric_by_mac(interval, "PuertoDestino"))[1]
	diff_layers = (get_metric_by_mac(interval, "layers"))[1]
	n_packets = (get_n_packets(interval))[1]

	return [macs,n_packets,diff_srcips,diff_dstips,diff_srcports,diff_dstports,diff_layers]


def load_data(maclist,data,prob):

	for k,m in enumerate(maclist):
		body = {
			"@timestamp": int(round(time.time() * 1000)),
			"mac":m,
			"n_packets": data[k][0],
			"diff_srcips": data[k][1],
			"diff_dstips": data[k][2],
			"diff_srcports": data[k][3],
			"diff_dstports": data[k][4],
			"diff_layers": data[k][5],
		}

		if prob:
			body['prob'] = prob[k]

		response = es.index(index = es_index_ml, doc_type=es_doc_type, body = body)

def get_bulk_pro_data(n):
	#gmm_model_size

	macs = []
	n_packets = []
	diff_srcips = []
	diff_dstips = []
	diff_srcports = []
	diff_dstports = []
	diff_layers = []

	body = {
    "query": {
        "match_all": {}
    }
	}


	body_n =  {
					   "query":{
					      "bool":{
					         "must":{
					            "range":{
					               "@timestamp":{
					                  "gte":int(round(time.time() * 1000)) - (n * 60000),
					                  # ini date
					                "lte":int(round(time.time() * 1000)),
					                  # end date
					                "format":"epoch_millis"
					               }
					            }
					         }
					      }
					   }
					   }
	
	result = es.search(index = es_index_ml, size = n,doc_type=es_doc_type, body = body_n)['hits']['hits']

	for document in result:
		macs.append(document['_source']['mac'])
		n_packets.append(document['_source']['n_packets'])
		diff_srcips.append(document['_source']['diff_srcips'])
		diff_dstips.append(document['_source']['diff_dstips'])
		diff_srcports.append(document['_source']['diff_srcports'])
		diff_dstports.append(document['_source']['diff_dstports'])
		diff_layers.append(document['_source']['diff_layers'])

	return [macs,n_packets,diff_srcips,diff_dstips,diff_srcports,diff_dstports,diff_layers]