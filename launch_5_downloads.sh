#!/bin/bash

start=$1
end=$2
spread=$(expr $end - $start)

startD=`date +%s`
echo "Started at: " `date`
((startD+=$spread/5))
echo "Expected at:" `date --date=@$startD`
step=$(expr $spread / 5)

count=$start

for ((i=0; i<4; i++))
do
    count2=$count
    ((count+=$step))
    python3 generate_block_table.py $count2 $count &
    sleep 0.04
done

count2=$count
((count+=$step))
python3 generate_block_table.py $count2 $count

sleep 10

python3 merge_results.py $start $count

echo "Done"

echo "Ended at: " `date`
