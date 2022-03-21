# Mapping (YARRRML to RML to RDF)
```bash
cd data
```

## Block
```bash
yarrrml-parser -i blocks.yarrrml.yml -o blocks.rml.ttl
java -jar _rmlmapper.jar -m blocks.rml.ttl -o turtle/blocks.ttl -s turtle
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

## Financial data
Setup
```
pip3 install yfinance
mkdir financial
```
Using it:
```
from get_financial_data import get_ticker_data
get_ticker_data('btc-usd')
```
