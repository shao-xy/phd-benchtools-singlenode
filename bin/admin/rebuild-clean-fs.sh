#!/bin/bash

mds_num=$1

function prompt()
{
	echo -e "\033[1;33m$@\033[0m"
}

function short_wait()
{
	prompt "Short wait - 10s"
	sleep 10
}

prompt "Unmount all possible clients"
#for i in 9 14 17 18 19; do
#	ssh node$i "sudo umount -f /mnt/bigmem-clients/*" &
#done
#wait
sudo umount -f /mnt/ceph-client-* &>/dev/null
set -e

short_wait

prompt "Stop all MDS instances"
sudo systemctl stop ceph-mds.target

short_wait

prompt "Force fail all MDS instances"
ceph mds fail 4
ceph mds fail 3
ceph mds fail 2
ceph mds fail 1
ceph mds fail 0

short_wait

prompt "Destroying file system"
ceph fs rm myfs --yes-i-really-mean-it

short_wait

prompt "Destroying OSD pool \"md\" and \"d\""
ceph osd pool rm md md --yes-i-really-really-mean-it
ceph osd pool rm d d --yes-i-really-really-mean-it

prompt "Creating new pool \"md\" and \"d\""
ceph osd pool create md 128 128
ceph osd pool create d 128 128

prompt "Creating new file system"
ceph fs new myfs md d

prompt "Starting MDS instances"
sudo systemctl restart ceph-mds.target

prompt "Set config standby_count_wanted"
ceph fs set myfs standby_count_wanted 0

if ! test -z "$mds_num"; then
	prompt "Setting multiple MDS"
	ceph mds set_max_mds $mds_num
fi

prompt "Done."
