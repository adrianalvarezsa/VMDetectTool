#!/bin/bash 

lines=$(sudo lsmod | egrep -i 'vbox(guest|video|sf)' | wc -l)

if [ "$lines" -ge 2 ]; then
	exit 0
else
	exit 5
fi
