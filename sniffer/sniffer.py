#!/usr/bin/python
import scapy.all as scapy
import socket
import json
import time
import requests

# Enumeration of the packet's layers
def enumeration(packet):
	yield packet.name
	while packet.payload:
		packet =packet.payload
		yield packet.name

# Epoch milliseconds calculator
epoch_millis = lambda: int(round(time.time() * 1000))

# Packet parser
def parser(packet):
	dictionary = {}
	# Timestamp identification for Grafana and ElasticSearch
	dictionary['@timestamp'] = epoch_millis()
	layers = ""
	# Agregation of all the packet's layers
	for i in enumeration(packet):
		if i == 'Raw':
			break
		if (layers == ""):
			layers = i
		layers += ',' + i
	dictionary['layers'] = layers
	# Agregation of specific packet's data
	try:
		dictionary['MacOrigen'] = getattr(packet.getlayer('Ethernet'),'src')
		dictionary['IpOrigen'] = getattr(packet.getlayer('IP'),'src')
		dictionary['IpDestino'] = getattr(packet.getlayer('IP'),'dst')
		if(packet.getlayer('TCP')):
			dictionary['TCPseq'] = getattr(packet.getlayer('TCP'),'seq')
			dictionary['PuertoOrigen'] = getattr(packet.getlayer('TCP'),'sport')
			dictionary['PuertoDestino'] = getattr(packet.getlayer('TCP'),'dport')
		if(packet.getlayer('UDP')):
			dictionary['PuertoOrigen'] = getattr(packet.getlayer('UDP'),'sport')
			dictionary['PuertoDestino'] = getattr(packet.getlayer('UDP'),'dport')

	except Exception:
		print('err')
	# Json creation and data sending
	json_data = json.dumps(dictionary)
	print(json_data)
	try:
		resp = requests.post("http://localhost:5001/save", data=json_data)
		print(resp.status_code, resp.reason)
	except Exception:
		print('error de conexion')

# Sniffer
scapy.sniff(filter='ip',prn=parser)