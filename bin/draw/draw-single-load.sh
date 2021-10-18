#!/bin/bash

if test $# -ne 2; then
	echo "Usage: $0 <dir> <mds_idx>"
	exit 1
fi

dir="$1"
idx=$2
targetfile="$dir/Load-mds$idx"
xrangemax=$(tail -n 1 $targetfile | awk '{print $1}')
xrangeV=[0:$xrangemax]
#x_1tic=

# TODO: yrange is arbitrary
yrangeV=[0:200000]

cat << EOF > draw.plt
set terminal pdfcairo lw 2 font "Times New Roman,26" size 4,3
#set key box bottom
set output "$dir/figs/Cluster-Load-MDS$idx.pdf"
set xlabel offset 0,0.5 "Epoch" font ",26"
set ylabel offset 0.5,0 "MDS Load" font ",26"
set xrange $xrangeV
set yrange $yrangeV
set format y '%.1s%c'
#set title offset 0,-0.5 "AI training" font "0,26"
#set ytics 15000
#set logscale y
set nokey
set xtics 0,400,1700 offset 1,0
set title "MDS load over time (Load-mds$idx)"

plot \
  "$targetfile" u 1:2 w l lw 1.5 lc rgb "blue" title "MDS-1",\
  "$targetfile" u 1:3 w l lw 1.5 lc rgb "cyan" title "MDS-2",\
  "$targetfile" u 1:4 w l lw 1.5 lc rgb "orange" title "MDS-3",\
  "$targetfile" u 1:5 w l lw 1.5 lc rgb "red" title "MDS-4",\
  "$targetfile" u 1:6 w l lw 1.5 lc rgb "green" title "MDS-5"

EOF


#cat draw.plt 
cat draw.plt | gnuplot
rm draw.plt
#pdfcrop output/IOPS-$suffix.pdf
