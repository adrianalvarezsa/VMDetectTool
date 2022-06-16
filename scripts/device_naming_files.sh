#!/bin/bash 

lines=$(ls -1 /dev/disk/by-id/ | egrep -i 'v(box|mware)' | wc -l)

if [ "$lines" -ge 1 ]; then
	exit 0
else
	exit 5
fi
