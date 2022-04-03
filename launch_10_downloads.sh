#!/bin/bash

start=`date +%s`
echo "Started at: " `date`
((start+=$1/25))
echo "Expected at:" `date --date=@$start`
step=$(expr $1 / 5)
count=400000

start_count=$count

for ((i=0; i<4; i++))
do
    count2=$count
    ((count+=$step))
    python3 analysis2.py $count2 $count &
    sleep 0.04
done

count2=$count
((count+=$step))
python3 analysis2.py $count2 $count

sleep 5

# python3 merge_results.py $start_count $count

echo "Done"

echo "Ended at: " `date`
