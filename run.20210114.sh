#!/bin/bash

function calculate() {
	./bin/admin/extract-sxy $1
	./bin/calc/genData $1
}

for i in $(seq 1 5); do
	./master fb_create_100k 1 $i nowait
	calculate log-1c-5m-fb_create_100k-ceph-${i}-20210114/ &
	sleep 5
done
wait
