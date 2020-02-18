#!/bin/bash



# Start first

# Automatic learn
while :
do
		qstat -u x1797a07  | grep "x1797a07"
        if [ $(qstat -u x1797a07  | grep "x1797a07" | wc -l ) -eq 0 ]; then
                echo **********************************done...
        fi
        sleep 60
done

