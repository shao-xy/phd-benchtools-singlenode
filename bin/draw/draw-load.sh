#!/bin/bash

if test $# -ne 1; then
	echo "Usage: $0 <dir>"
	exit 1
fi

exedir=$(dirname $0)
targetdir=$1

for i in 1 2 3 4 5; do
	bash ${exedir}/draw-single-load.sh $targetdir $i
done
