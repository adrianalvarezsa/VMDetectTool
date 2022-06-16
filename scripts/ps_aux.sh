#!/bin/bash 

lines=$(ps aux | egrep -i 'v(box|irtualbox|mware)' | grep -v grep | wc -l)

if [ "$lines" -ge 1 ]; then
	exit 0
else
	exit 5
fi
