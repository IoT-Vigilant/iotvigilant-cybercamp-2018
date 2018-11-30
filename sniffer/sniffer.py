#!/usr/bin/python3
from scapy.all import *
import socket
import json
import time
import requests
import _thread

# Enumeration of the packet's layers
def enumeration(packet):
	yield packet.name
	while packet.payload:
		packet =packet.payload
		yield packet.name

# Epoch milliseconds calculator
epoch_millis = lambda: int(round(time.time() * 1000))

def send(data):
	try:
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		resp = requests.post("http://192.168.43.118:5001/save", data=data, headers= headers)
		return resp.status_code
	except Exception:
		print('error de conexion')

data_list = []
time_old = 0

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

	except Exception as e:
		print(str(e))
	# Json creation and data sending
	json_data = json.dumps(dictionary)
	time = epoch_millis()
	global data_list
	global time_old
	data_list.append(json_data)
	if (time_old == 0):
		time_old = time 
	elif ((time - time_old) > 10000):
		try:
			_thread.start_new_thread(send,(json.dumps(data_list),))
		except Exception as e:
			print(str(e))
		data_list = []
		time_old = 0

# Sniffer
sniff(filter='ip',prn=parser)