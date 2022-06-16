#!/bin/bash 

DIR=/sys/module/vmw_balloon

if [ -d "$DIR" ]; then
	exit 0
else
	exit 5
fi
