#!/bin/bash 

interfaz_mac=$(ls /sys/class/net/ | grep -E '^e\w')
MAC_8=$(head -c 8 /sys/class/net/$interfaz_mac/address) 
MAC=$(cat /sys/class/net/$interfaz_mac/address)

case $MAC_8 in 
	00:1c:14)
	exit 0
	;;
	00:50:56)
	exit 0
	;;
	00:0c:29)
	exit 0
	;;
	00:05:69)
	exit 0
	;;
	08:00:27)
	exit 0
	;;
	52:54:00)
	exit 0
	;;
	00:14:4f)
	exit 0
	;;
	00:21:f6)
	exit 0
	;;
	00:0f:4b)
	exit 0
	;;
	*)
	exit 5
	;;
esac
