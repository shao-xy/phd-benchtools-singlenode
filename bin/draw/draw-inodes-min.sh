#!/bin/bash

if test $# -ne 1; then
	echo "Usage: $0 <dir>"
	exit 1
fi

dir=$1
if test ! -d $dir/figs/; then
	mkdir $dir/figs
fi
strategy=$(basename $1)

cat << EOF > draw.plt
set terminal pdfcairo lw 2 font "Times_New_Roman,16" size 6,4
set key box
set output "$1/figs/Inodes-${dir////_}.pdf"
set xlabel "time/min"
set ylabel "# of Inodes"
set format y '%.1s%c'
set xrange [0:$(tail -n 1 $dir/tempIOPS.txt | awk '{print $1}')]
set title "#Inodes over time($strategy)"
plot "$dir/Inodes-mds0-minute" with lines title " MDS-0" lw 2 lt 1,\
    "$dir/Inodes-mds1-minute" with lines title " MDS-1" lt 2,\
    "$dir/Inodes-mds2-minute" with lines title " MDS-2" lt 3,\
    "$dir/Inodes-mds3-minute" with lines title " MDS-3" lt 4,\
    "$dir/Inodes-mds4-minute" with lines title " MDS-4" lt 5
EOF

cat draw.plt | gnuplot
rm draw.plt
