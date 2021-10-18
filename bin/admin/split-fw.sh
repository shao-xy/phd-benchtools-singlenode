#!/bin/bash

rm -f client-log/client-fw-*.log
awk -F 'SXYMODMDS_FORWARDTRACE' '{ print $2 }' client-log/client-fw.log \
| awk '{print $5 " " $7 " " $9 " " (100.0*$9/$7)}' \
| while read line; do
	read fwdnum totallat fwdlat ratio <<< "$line"
	echo -e "$fwdnum\t$totallat\t$fwdlat\t$ratio" >> client-log/client-fw-${fwdnum}.log
done
