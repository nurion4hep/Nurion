#!/bin/bash

for i in `seq 1 3`;do


while :
do
        echo $(date +%s%N)
        if [ $(qstat -u jiwoong | grep "jiwoong" | wc -l ) -eq 0]; then
                qsub -q cms run$i\.sh
                echo **************************************************************************start...
                break
        fi
        sleep 100
done
done
