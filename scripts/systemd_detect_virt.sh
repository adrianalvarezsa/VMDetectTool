#!/bin/bash 

line=$(systemd-detect-virt --vm)

if [ "$line" == "none" ]; then
	exit 5
else
	exit 0
fi
