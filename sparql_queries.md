# SPARQL queries (in our sample)

## General queries

### Prefixes of requests
```
PREFIX ex: <https://example.org/udem/ift6056/>
PREFIX schema: <https://schema.org/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
```

### Count number of blocks
```
SELECT (COUNT(?block) AS ?count)
WHERE { 
	?block a schema:Block .
}
```

### Count number of transactions for all blocks
```
SELECT ?block (COUNT(?transaction) AS ?nb_transactions)
WHERE { 
	?transaction a schema:Transaction ;
		ex:block ?block .
}
GROUP BY ?block
ORDER BY DESC(?nb_transactions)
```

### Count number of utxos in outputs of all transactions of each block
```
SELECT ?block (COUNT(?utxo) AS ?nb_utxos)
WHERE { 
	?utxo a schema:UTXO .
    ?transaction a schema:Transaction ;
		ex:block ?block ;
    	ex:outputs ?utxo .
}
GROUP BY ?block
ORDER BY DESC(?nb_utxos)
```

### Count number of utxos in inputs of all transactions of each block
```
SELECT ?block (COUNT(?utxo) AS ?nb_utxos)
WHERE { 
	?utxo a schema:UTXO ;
		ex:input ?transaction .
    ?transaction a schema:Transaction ;
		ex:block ?block .
}
GROUP BY ?block
ORDER BY DESC(?nb_utxos)
```

### Get top 10 UTXO based on their value
```
SELECT ?address ?value
WHERE { 
    ?utxo a schema:UTXO ;
          ex:value ?value ;
          ex:address ?address .
}
ORDER BY DESC(?value)
LIMIT 10
```

### Get total value of satoshi each address hold
```
SELECT ?address (SUM(?value) as ?total)
WHERE { 
    ?utxo a schema:UTXO ;
          ex:value ?value ;
          ex:address ?address .
}
GROUP BY ?address
ORDER BY DESC(?total)
```

### Count number of transactions for each address
```
PREFIX ex: <https://example.org/udem/ift6056/>
PREFIX schema: <https://schema.org/>

SELECT ?address (COUNT(?transaction) as ?nb_transactions)
WHERE {
    SELECT DISTINCT ?address ?transaction
    WHERE { 
        ?transaction a schema:Transaction ;
            ex:block ?block ;
            ex:outputs ?utxo .
        ?utxo a schema:UTXO ;
            ex:value ?value ;
            ex:address ?address .
    }
}
GROUP BY ?address
ORDER BY DESC(?nb_transactions)
```

### Get all transactions after a specific time
```
SELECT ?block ?transaction ?time_gmt
WHERE { 
    ?transaction a schema:Transaction ;
		ex:block ?block ;
        ex:outputs ?utxo .
    ?block a schema:Block ;
        ex:time_gmt ?time_gmt .
    
    FILTER(?time_gmt > "2022-02-03T06:06:06"^^xsd:dateTime)
}
```