#!/bin/bash 

if [ -d /proc/scsi ]; then

    lines=$(cat /proc/scsi/scsi | egrep -i 'v(box|mware)' | wc -l)
    
    if [ "$lines" -ge 1 ]; then
	    exit 0
    else
	    exit 5
    fi	    
else
    exit 5
fi
