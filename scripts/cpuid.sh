#!/bin/bash 

SCRIPT=$(readlink -f $0);
dir=`dirname $SCRIPT`;

if [ -f $dir/cpuid.out ]; then
	lines=$($dir/cpuid.out | grep vmware | wc -l)
else
	gcc $dir/cpuid.c -o $dir/cpuid.out
	lines=$($dir/cpuid.out | grep vmware | wc -l)
fi

if [ "$lines" -eq 1 ]; then
	exit 0
else
	exit 5
fi
