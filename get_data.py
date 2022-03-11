import json
from urllib.request import urlopen

import numpy as np
import pandas as pd

# Utils

def printJSON(j) :
    print(json.dumps(j, indent=4, sort_keys=True))

# Get Data

def getBlock(block_hash) :
	block_url = 'https://blockchain.info/rawblock/' + block_hash

	response = urlopen(block_url)
	data_json = json.loads(response.read())
	return data_json

def getTransaction(tx_hash) :
	tx_url = 'https://blockchain.info/rawtx/' + tx_hash

	response = urlopen(tx_url)
	data_json = json.loads(response.read())
	return data_json

def totalValueOfTransaction(transaction) : 
	total = 0
	for o in transaction['out'] :
		total = total + o['value']
	return total

def isCoinbase(transaction) :
	return len(transaction['inputs']) == 1 and transaction['inputs'][0]['prev_out']['value'] == 0

def satoshiToBTC(satoshi) :
	return satoshi/100000000

def getAllTransactionsOfAddress(address) :
	address_url = 'https://blockchain.info/rawaddr/' + address

	response = urlopen(address_url)
	data_json = json.loads(response.read())
	return data_json
