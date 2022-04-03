import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

from get_data import *
from get_financial_data import *

def diff_estimate(hash):
    """
     Count the amounts of 0s at the start of a hash to put an upper-bound on the difficulty
     Difficulty reevaluation is every 20160 minutes, so theoretically about 2016 blocks
     Hence, taking the min value of this over 2016 consecutive blocks can gives a reasonable difficulty estimate
     From this we can then reverse-engineer the approximate hashpower of the network 
     (TODO, will do so later)
    """
    return len(hash)-len(hash.lstrip('0'))

def sanitize_height(from_height, to_height):
    """ CQFD """
    if from_height > to_height: from_height, to_height = to_height, from_height
    return max(from_height, 0), min(to_height, getBlockLast()['height'])

def get_value(tx_out):
    """
     Get the total value of a transaction by counting what every output UTXO of the transaction recieves
    """
    return sum([out['value'] for out in tx_out])

def gather_statistics(from_height, to_height, interests, tx_interests):
    """
     gather block information for blocks ranging from from_height to to_height
     interests: statistics gathered (NOT resiliant to change, check code)
     tx_interests: statistics gathered for each transaction (NOT resiliant to change, check code)
     OUTPUT: Pandas DataFrame with data
        columns: the interests then count, mean, std, min, max for each tx_interests
        rows: 1 per block

     Statistics gathered can then be cross examined for possible correlation
     Time taken: 5 blocks per second, seems to be linear
        Limited by web requests (parallelise requests maybe? might hit server limits)
    """
    from_height, to_height = sanitize_height(from_height, to_height)
    interests = interests.split(' ')
    tx_interests = tx_interests.split(' ')
    interests = interests + [a+'_'+b for a in tx_interests for b in 'count mean std min max'.split(' ')]
    block_data = pd.DataFrame(columns=interests, index=range(from_height, to_height))
    #block_data = np.zeros((to_height-from_height, len(interests)))
    print(from_height, to_height)
    
    for height in range(from_height, to_height):
        if not height%1000 and height!=from_height: block_data.to_csv(f"data_btc/blocks_{from_height}_{height}.csv")
        try:
            block = getBlockN(height)
        except:
            continue

        hash = int(block['hash'], 16)
        difficulty = diff_estimate(block['hash'])

        # interests for the transactions: vin_sz vout_sz fee lock_time value
        transac_data = np.zeros((block['n_tx'], len(tx_interests)))
        for i, tx in enumerate(block['tx']):
            tx_data = [tx[param] for param in tx_interests[:4]]
            value = get_value(tx['out'])
            transac_data[i, :] = tx_data + [value]

        transac_data = pd.DataFrame(transac_data).describe(percentiles=[]).drop(index='50%')
        transac_data = list(transac_data.to_numpy().flatten())
        
        data = [hash] + [block[i] for i in interests[1:7]] + [difficulty] + transac_data
        block_data.loc[height, :] = data
        #block_data[height-from_height, :] = data

    # TODO add time taken to validate block (next_block["time"] - block["time"])
    # look at spread around 10 minutes

    return block_data


if __name__ == "__main__":
    if len(sys.argv)!=3: 
        print("ERROR inproper argument amount")
        quit()

    from_height, to_height = [int(i) for i in sys.argv[1:]]

    # print("Estimated time (minutes):", (to_height-from_height)//(5*60))

    interests = 'hash ver time bits fee nonce n_tx difficulty'
    tx_interests = 'vin_sz vout_sz fee lock_time value'
    
    block_data = gather_statistics(from_height, to_height, interests, tx_interests)

    block_data.to_csv(f"data_btc/blocks_{from_height}_{to_height}.csv")

    # print("done")
