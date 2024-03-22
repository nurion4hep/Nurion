#!/bin/bash


timestamp=`date +%Y%m%d%H%M`
i=1

# Start first

# Automatic learn
while :
do
        qstat -u x1797a07  | grep "x1797a07"
        if [ $(qstat -u x1797a07  | grep "x1797a07" | wc -l ) -eq 0 ]; then
                echo **********************************done...
			file=run0$i\.sh
			echo $file
			qsub $file
               	i=`expr $i + 1`
        fi
        sleep 60
done

