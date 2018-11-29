from datetime import datetime
from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch


'''
	API REST Server 
'''

__author__ = "IoT Vigilant"

es_host = "localhost"
es_port = 9200
es_index = "rawdata"
es_doc_type = "ts"

es = Elasticsearch([{'host': es_host, 'port': es_port}])

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    results = es.indices.get_alias("*")
    return jsonify(results)

@app.route('/', methods=['POST'])
def index():
     result = es.index(index=es_index, doc_type='title', id=slug, body=body)
    return jsonify(results)




app.run(port=5001, debug=True)