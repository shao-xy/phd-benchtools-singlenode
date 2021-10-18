#!/bin/bash

if test ! -d handle; then
	mkdir handle
fi

grep SXYMODMDS_FORWARDTRACE client-log/client.log | awk -F 'SXYMODMDS_FORWARDTRACE' '{ print $2 }' | awk '{print $5}' > handle/fwd_num
grep SXYMODMDS_FORWARDTRACE client-log/client.log | awk -F 'SXYMODMDS_FORWARDTRACE' '{ print $2 }' | awk '{print $7}' > handle/total_lat
