#!/usr/bin/python
import scapy.all as scapy
import socket
import json

# Enumeration of the packet's layers
def enumeration(packet):
	yield packet.name
	while packet.payload:
		packet =packet.payload
		yield packet.name

# # Mapping between the protocol number and its name
# def protocol(number):
# 	table = {num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}
# 	return table[number]

# Packet parser
def parser(packet):
	dict = {}
	layers = ""
	# Agregation of all the packet's layers
	for i in enumeration(packet):
		if i == 'Raw':
			break
		if (layers == ""):
			layers = i
		layers += ',' + i
	dict['layers'] = layers
	# Agregation of specific packet's data
	try:
		dict['Mac-origen'] = getattr(packet.getlayer('Ethernet'),'src')
		dict['IP-origen'] = getattr(packet.getlayer('IP'),'src')
		dict['IP-destino'] = getattr(packet.getlayer('IP'),'dst')
		if(packet.getlayer('TCP')):
			dict['TCP-seq'] = getattr(packet.getlayer('TCP'),'seq')
			dict['Puerto-origen'] = getattr(packet.getlayer('TCP'),'sport')
			dict['Puerto-destino'] = getattr(packet.getlayer('TCP'),'dport')
		if(packet.getlayer('UDP')):
			dict['Puerto-origen'] = getattr(packet.getlayer('UDP'),'sport')
			dict['Puerto-destino'] = getattr(packet.getlayer('UDP'),'dport')

	except Exception:
		print('err')
	# Json creation and data sending
	json_data = json.dumps(dict)
	print(json_data)

# Sniffer
scapy.sniff(filter='ip',prn=parser)