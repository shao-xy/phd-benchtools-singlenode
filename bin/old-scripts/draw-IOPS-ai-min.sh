#!/bin/bash

#if test $# -ne 1; then
#	echo "Usage: $0 <dir>"
#	exit 1
#fi

dir=../../../
compilation=${dir}workload-compilation-withdata
tar=${dir}workload-tar
zipf=${dir}workload-zipfian
ai=${dir}workload-ai
sharedweb=${dir}workload-shared-web
xrangeV=[0:50]
yrangeV=[0:75000]
suffix="AI"
ps=0.75

cat << EOF > draw.plt
set terminal pdfcairo lw 2 font "Times New Roman,26" size 4,3
#set key box bottom
set output "output/IOPS-$suffix.pdf"
set xlabel offset 0,0.5 "time/min" font ",26"
set ylabel offset 0.5,0 "Aggregated IOPS" font ",26"
set xrange $xrangeV
set yrange $yrangeV
set format y '%.1s%c'
#set title offset 0,-0.5 "AI training" font "0,26"
set ytics 15000
set nokey
#set xtics 0,5,50 offset 1,0

plot \
  "$ai/ceph/CV.txt" every ::0::50 u 1:2 w l dt 1 lw 1.5 lc rgb "blue" title "Ceph-Original",\
  "$ai/greedyspill/CV.txt" every ::0::50 u 1:2 w l dt 1 lw 1.5 lc rgb "cyan" title "Ceph-Mantle",\
  "$ai/ifenable/CV.txt" every ::0::50 u 1:2 w l dt 1 lw 1.5 lc rgb "orange" title "Lunule-Light",\
  "$ai/lunule1.1/CV.txt" every ::0::50 u 1:2 w l dt 1 lw 1.5 lc rgb "red" title "Lunule"

EOF


#cat draw.plt 
cat draw.plt | gnuplot
rm draw.plt
pdfcrop output/IOPS-$suffix.pdf
