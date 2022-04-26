# A multi-approach analysis of the Bitcoin Blockchain
This breaks down into 2 parts: a knowledge graph and a statistical analysis.
# Knowledge Graph Mapping (YARRRML to RML to RDF)
```bash
cd data
```

## Block
```bash
yarrrml-parser -i blocks.yarrrml.yml -o blocks.rml.ttl
java -jar _rmlmapper.jar -m blocks.rml.ttl -o turtle/blocks.ttl -s turtle
```

## Address
```bash
yarrrml-parser -i addresses.yarrrml.yml -o addresses.rml.ttl
java -jar _rmlmapper.jar -m addresses.rml.ttl -o turtle/addresses.ttl -s turtle
```

## Transaction
```bash
yarrrml-parser -i transactions.yarrrml.yml -o transactions.rml.ttl
java -jar _rmlmapper.jar -m transactions.rml.ttl -o turtle/transactions.ttl -s turtle
```

## UTXO
```bash
yarrrml-parser -i utxos.yarrrml.yml -o utxos.rml.ttl
java -jar _rmlmapper.jar -m utxos.rml.ttl -o turtle/utxos.ttl -s turtle

yarrrml-parser -i coinbase_utxos.yarrrml.yml -o coinbase_utxos.rml.ttl
java -jar _rmlmapper.jar -m coinbase_utxos.rml.ttl -o turtle/coinbase_utxos.ttl -s turtle
```

# Statistical analysis
The core of this analysis can be found in the `statistical_analysis` notebook. This notebook gets the block data from the `data_btc` folder.

The `btc_eth` notebook contains the comparisons between the Bitcoin and Ethereum values.

## Requirements
```
pip3 install yfinance pandas numpy matplotlib
```

## Getting the block data
This can be automated by running the deseigned script. This script downloads the data on 5 threads concurrently to speed it up. It was notted that any more thread would result in `blockchain.info` DDoS protection activating and kicking all of our connections.

For the small block, at the start of the blockchain it can go as fast as 3 per second. However, for the bigger ones at the end it can slow down to 3 seconds per block. 

```
./launch_5_downloads.sh start end
```

`start` and `end` are the block height at which to start downloading and the one at which to stop. It is recommented to keep both a factor of 100 to avoid rounding-related errors.

## Running the notebook
Input the `start` and `end` heights selected above into the second cell of the notebook and run all.

## Times of interest
We studied the range from `480000` to `540000` for the first bitcoin hype late 2017 and included this data for demonstration purposes.

We also studied and included the range from `630000` to `705000` for the effect of the chinese ban early 2020.

## Saved figures
The figures used in the report are all saved in the `figures` folder.