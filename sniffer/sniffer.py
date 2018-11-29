#!/usr/bin/python
import scapy.all as scapy
import scapy_http.http
import socket

def expand(packet):
	yield packet.name
	while packet.payload:
		packet =packet.payload
		yield packet.name

def printer(packet):
	for i in expand(packet):
		if i == 'Raw':
			break
		else:
			print(i)
			diccionario = packet.getlayer(i).fields
			print(diccionario)

scapy.sniff(filter='ip',prn=printer)