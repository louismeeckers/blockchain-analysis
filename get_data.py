import json
from urllib.request import urlopen
from urllib.error import HTTPError
import numpy as np
import pandas as pd

# Utils

def printJSON(j):
    print(json.dumps(j, indent=4, sort_keys=True))

# Get Data

def getBlock(block_hash):
	block_url = 'https://blockchain.info/rawblock/' + block_hash

	response = urlopen(block_url)
	data_json = json.loads(response.read())
	return data_json

def request(block_url):
    try:
        return urlopen(block_url)
    except HTTPError as e:
        if e.code == 429:
            print("Got 429")
            return request(block_url)
        raise

def getBlockN(n):
    block_url = f'https://blockchain.info/block-height/{n}?format=json'
    response = request(block_url)
    data_json = json.loads(response.read())['blocks']

    if len(data_json) == 0:
        print("WARNING no block this deep")
        return {}
    elif len(data_json) > 1:
        print("WARNING multiple blocks at this depth (first one returned)")

    return data_json[0]

def getBlockLast():
	block_url = 'https://blockchain.info/latestblock'
	response = urlopen(block_url)
	data_json = json.loads(response.read())
	return getBlockN(data_json['height'])

def getPreviousBlock(block):
	return getBlock(block['prev_block'])

def getNextBlock(block):
	return getBlock(block['next_block'][0])

def getTransaction(tx_hash):
	tx_url = 'https://blockchain.info/rawtx/' + tx_hash

	response = urlopen(tx_url)
	data_json = json.loads(response.read())
	return data_json

def totalValueOfTransaction(transaction): 
	total = 0
	for o in transaction['out']:
		total = total + o['value']
	return total

def isCoinbase(transaction):
	# return len(transaction['inputs']) == 1 and transaction['inputs'][0]['prev_out']['value'] == 0
	return transaction['inputs'][0]['script'] == ''

def satoshiToBTC(satoshi):
	return satoshi/100000000

def getAllTransactionsOfAddress(address):
	address_url = 'https://blockchain.info/rawaddr/' + address

	response = urlopen(address_url)
	data_json = json.loads(response.read())
	return data_json
