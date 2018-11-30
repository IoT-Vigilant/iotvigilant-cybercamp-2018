#!/usr/bin/python3

import time, argparse 

from datetime import datetime
from flask import Flask, jsonify, request, Response
from elasticsearch import Elasticsearch


"""
===================================
API REST- Local Server
===================================
Get information from IoTVigilant sniffers and feed Elasticsearch with it
--> Todo: Provides authentication and session control
"""
listen_port = 5001
es_host = "localhost"
es_port = 9200
es_index = "rawdata"
es_doc_type = "ts"

def config_params():
	"""
	Configure the parameters used to connect to the Elasticsearch and the port where the server is going to listen
	"""
	global listen_port, es_host, es_port

	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('--elasticsearch-host', action='store',
						dest='es_host',
						default='localhost')
	arg_parser.add_argument('--elasticsearch-port', action='store',
						dest='es_port',
						default=9200, type=int)
	arg_parser.add_argument('--listen-port', action='store',
						dest='listen_port',
						default=5001, type=int)
	parameters = arg_parser.parse_args()

	if "IOTV_ES_HOST" in os.environ:
		parameters.es_host = os.getenv("IOTV_ES_HOST")
	if "IOTV_ES_PORT" in os.environ:
		parameters.es_port = os.getenv("IOTV_ES_PORT")
	if "IOTV_LISTEN_PORT" in os.environ:
		parameters.listen_port = os.getenv("IOTV_LISTEN_PORT")
	
	es_host = parameters.es_host
	es_port = parameters.es_port
	listen_port = parameters.listen_port

config_params()

# Elasticsearch instance
es = Elasticsearch([{'host': es_host, 'port': es_port}])
# Flask instance
app = Flask(__name__)


# Receives packets data from sniffer
@app.route('/save', methods=['POST'])
def index_post():
	if request.json: # if request body is json
		for body in request.json:
			print (body)
			# feeds 
			result = es.index(index=es_index, doc_type=es_doc_type, body=body)
			
		return Response("{ }", status=201, mimetype='application/json')
	return Response("{ }", status=400, mimetype='application/json')

app.run(host='0.0.0.0', port=listen_port, debug=True)