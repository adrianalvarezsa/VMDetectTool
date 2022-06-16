#!/bin/bash 

SCRIPT=$(readlink -f $0);
dir=`dirname $SCRIPT`;
 
sudo python3 $dir/disk_size.py
