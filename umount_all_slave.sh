#!/bin/bash

for i in $(seq 1 100); do
	sudo umount -f /mnt/ceph-client-$i
done
