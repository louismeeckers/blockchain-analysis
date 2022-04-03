import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

def merge(from_height, to_height, step=1000):
    block_data = [pd.read_csv(f"data_btc/blocks_{i}_{i+step}.csv", index_col=0) for i in range(from_height, to_height, step)]
    result = pd.concat(block_data)
    result.to_csv(f"data_btc/blocks_{from_height}_{to_height}.csv")

if __name__ == "__main__":
    if len(sys.argv)!=3: 
        print("ERROR inproper argument amount")
        quit()

    from_height, to_height = [int(i) for i in sys.argv[1:]]

    step = (to_height-from_height)//5

    merge(from_height, to_height, step)
    