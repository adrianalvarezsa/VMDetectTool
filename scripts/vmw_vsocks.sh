#!/bin/bash 

DIR1=/sys/module/vmw_vsock_virtio_transport_common
DIR2=/sys/module/vmw_vsock_vmci_transport



if [ -d "$DIR1" ] || [ -d "$DIR2" ]; then
	exit 0
else
	exit 5
fi
