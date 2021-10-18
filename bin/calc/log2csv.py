#!/usr/bin/env python3

import sys
import argparse

# 10 seconds for the default epoch
EPOCH_LENGTH = 10

def time_delta(old, new):
	oh, om, os = old.split(':')
	oh, om, os = int(oh), int(om), float(os)
	nh, nm, ns = new.split(':')
	nh, nm, ns = int(nh), int(nm), float(ns)
	return (nh - oh) * 3600 + (nm - om) * 60 + (ns - os)

def print_epoch(epoch, mds_load, target_load, targets, exports, reexports, requests):
	print(','.join((str(epoch), *mds_load, target_load, *targets)))
	for rank in range(len(exports)):
		rank_exports = exports[rank]
		for pop, dirname, success, se, dt, qt, et in rank_exports:
			line = ',' * (7 + rank)
			line += pop
			line += ',' * (5 - rank)
			line += dirname
			if success:
				line += ',%d,%.6f,%.6f,%.6f' % (se, dt, qt, et)
			print(line)

	for rank in range(len(reexports)):
		rank_reexports = reexports[rank]
		for pop, dirname, success, se, dt, qt, et in rank_reexports:
			line = ',' * (7 + rank)
			line += pop + '(r' + (not success and 'c' or '') + ')'
			line += ',' * (5 - rank)
			line += dirname
			if success:
				line += ',%d,%.6f,%.6f,%.6f' % (se, dt, qt, et)
			print(line)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('targetfile', help='target file to analyze')
	args = parser.parse_args()

	# MxL stands for MDS.x's Load
	# TargetL stands for Target Load
	# Ex stands for Export to MDS.x
	# DN stands for Directory Name
	# SE stands for Starting Epoch
	# DT stands for Decision Time in this epoch
	# QT stands for Queueing Time in this epoch
	# ET stands for Exporting Time in this epoch
	print('Epoch,M0L,M1L,M2L,M3L,M4L,TargetL,E0,E1,E2,E3,E4,DN,SE,DT,QT,ET')
	fin = open(args.targetfile, 'r')
	if not fin:	raise 'Cannot open file.'

	rank = int(args.targetfile.split('.')[1].split('-')[0])

	epoch = 0
	last_ts = '0:0:0.0'

	mds_load = [''] * 5
	target_load = ''
	targets = [''] * 5

	exports = [[],[],[],[],[]]
	reexports = [[],[],[],[],[]]

	reexport_from = -1

	requests = {}
	

	while True:
		line = fin.readline()
		if not line:
			break
		items = line.strip().split()

		# Skip client requests first
		if items[6] == 'dispatch_client_request':
			reqpath = items[10]
			try:
				requests[reqpath] += 1
			except KeyError:
				requests[reqpath] = 1
			continue

		# Next epoch?
		ts = float(items[1].split(':')[-1])
		ts = items[1]
		if time_delta(last_ts, ts) > 9.5:
			if epoch != 0:
				print_epoch(epoch, mds_load, target_load, targets, exports, reexports, requests)
			epoch += 1
			last_ts = ts
			mds_load = [''] * 5
			target_load = ''
			targets = [''] * 5
			exports = [[],[],[],[],[]]
			reexports = [[],[],[],[],[]]
			requests = {}

		# Exception: items[5]
		if items[5] == 'export_finish':
			dirname = items[6]
			qtime = items[9]
			etime = items[13]
			ftime = items[16]
			delta_epoch = int(items[-1]) - int(items[-3])
			if delta_epoch == 0:
				# This epoch
				export_item = None
				for rank in range(len(exports)):
					rank_exports = exports[rank]
					for export in rank_exports:
						if export[1] == dirname:
							export_item = export
							break
					if export_item:
						break
				for rank_reexports in reexports:
					for export in rank_reexports:
						if export[1] == dirname and export[2]:
							export_item = export
							break
					if export_item:
						break
				if not export_item:
					# Not found??
					raise BaseException('Unexpected export finish item: ' + dirname)

				decision = time_delta(last_ts, qtime)
				wait = time_delta(qtime, etime)
				export = time_delta(etime, ftime)
				export_item[2] = True
				export_item[3] = 0 # Means epoch offset here
				export_item[4] = decision
				export_item[5] = wait
				export_item[6] = export
			else:
				# From previous epochs
				decision = time_delta(last_ts, qtime) + delta_epoch * EPOCH_LENGTH 
				wait = time_delta(qtime, etime)
				export = time_delta(etime, ftime)

				# No Tracing
				line = ',' * 12
				line += '%s,-%d,%.6f,%.6f,%.6f' % (dirname, delta_epoch, decision, wait, epoch)
				print(line)

			continue

		stage = items[6]
		if stage == 'prep_rebalance':
			if items[7] == '(0)' and items[9] != '0':
				# Now this information is about last epoch.
				# However, this epoch's information is not shown.
				line = ',' * (6 + rank)
				line += 'C%s: %s' % (items[9], items[12])
				print(line)
			elif items[7] == '(2)' and items[8].startswith('mds.'):
				rank = int(items[8].split('.')[-1])
				mds_load[rank] = items[10]
			elif items[7] == '(3)':
				if items[8] == 'total_load':
					target_load = items[-1]
				elif items[8] == 'my_load' and items[9] == 'is' and items[10] == 'small':
					pass
		elif stage == 'prep_rebalance(6)':
			if items[7] != 'targets': continue
			rank = int(items[8].split('.')[-1])
			targets[rank] = items[10]
		elif stage == 'try_rebalance':
			if items[7] == '(5)':
				pop = items[11]
				rank = int(items[13].split('.')[-1])
				dirname = items[17].rstrip('/')
				exports[rank].append([pop,dirname,False,0,0,0,0])
			if items[7] == '(3)':
				if items[8] == 'considering':
					reexport_from = int(items[-1])
				elif items[8] == 'can\'t':
					rank = reexport_from
					dirname = items[12].rstrip('/')
					pop = items[-1]
					reexports[rank].append((pop, dirname, False, 0, 0, 0, 0))
					reexport_from = -1
				elif items[8] == 'Have':
					rank = int(items[-1].split('.')[-1])
					assert(rank == reexport_from)
					dirname = items[13].rstrip('/')
					pop = items[9]
					reexports[rank].append([pop, dirname, True, 0, 0, 0, 0])
					reexport_from = -1

	print_epoch(epoch, mds_load, target_load, targets, exports, reexports, exports)

	fin.close()
	return 0

if __name__ == '__main__':
	sys.exit(main())
