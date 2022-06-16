#!/bin/bash 

lines=$(sudo dmesg | egrep -i 'v(box|irtualbox|mware)' | wc -l)

if [ "$lines" -ge 2 ]; then
	exit 0
else
	exit 5
fi
