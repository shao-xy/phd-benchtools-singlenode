#!/bin/bash

if test $# -ne 1; then
	echo "Usage: $0 <dir>"
	exit 1
fi

dir=$1

for i in 1 2 3 4 5; do
	grep "prep_rebalance (2)" $dir/mds-log/mds$i.log | cut -b 86- > $dir/mds$i-load.log
done
