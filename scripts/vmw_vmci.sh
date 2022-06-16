#!/bin/bash 

DIR=/sys/module/vmw_vmci

if [ -d "$DIR" ]; then
	exit 0
else
	exit 5
fi
