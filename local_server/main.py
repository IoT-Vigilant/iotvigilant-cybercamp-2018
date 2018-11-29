from datetime import datetime
from flask import Flask, jsonify, request, Response
from elasticsearch import Elasticsearch

"""
===================================
API REST- Local Server
===================================
--> Processes requests from IoT Sniffer and feeds Elasticsearch
--> Todo: Provides authentication and session control
--> 
"""

__author__ = "IoT Vigilant"

# Params
es_host = "localhost"
es_port = 9200
es_index = "rawdata"
es_doc_type = "ts"

# Elasticsearch instance
es = Elasticsearch([{'host': es_host, 'port': es_port}])
# Flask instance
app = Flask(__name__)


# Receive packets data from sniffer
@app.route('/save', methods=['POST'])
def index_post():
	if request.json: # if request body is json
		mydata = request.json
		# feeds 
		result = es.index(index=es_index, doc_type=es_doc_type, body=mydata)
		print(result)
	
	return Response(result, status=201, mimetype='application/json')


app.run(port=5001, debug=True)