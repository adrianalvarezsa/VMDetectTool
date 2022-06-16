#!/bin/bash 

lines=$(hostnamectl | egrep -i 'v(irtualbox|mware)' | wc -l)

if [ "$lines" -ge 1 ]; then
	exit 0
else
	exit 5
fi
