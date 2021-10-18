#!/bin/bash

grep "\(prep_rebalance (0)\|prep_rebalance (2)\|prep_rebalance (3)\|prep_rebalance(6)\|try_rebalance (3)\|try_rebalance (5)\|export_finish\|dispatch_client_request\)" mds5.log > mds.0-bal.log
grep "\(prep_rebalance (0)\|prep_rebalance (2)\|prep_rebalance (3)\|prep_rebalance(6)\|try_rebalance (3)\|try_rebalance (5)\|export_finish\|dispatch_client_request\)" mds2.log > mds.1-bal.log
grep "\(prep_rebalance (0)\|prep_rebalance (2)\|prep_rebalance (3)\|prep_rebalance(6)\|try_rebalance (3)\|try_rebalance (5)\|export_finish\|dispatch_client_request\)" mds3.log > mds.2-bal.log
grep "\(prep_rebalance (0)\|prep_rebalance (2)\|prep_rebalance (3)\|prep_rebalance(6)\|try_rebalance (3)\|try_rebalance (5)\|export_finish\|dispatch_client_request\)" mds1.log > mds.3-bal.log
grep "\(prep_rebalance (0)\|prep_rebalance (2)\|prep_rebalance (3)\|prep_rebalance(6)\|try_rebalance (3)\|try_rebalance (5)\|export_finish\|dispatch_client_request\)" mds4.log > mds.4-bal.log

exit 0

for i in 0 1 2 3 4; do
	./log2csv.py mds.$i-bal.log > mds.$i-bal.csv
done
