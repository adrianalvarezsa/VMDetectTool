#!/bin/bash 

DIR=/sys/module/vmwgfx

if [ -d "$DIR" ]; then
	exit 0
else
	exit 5
fi
