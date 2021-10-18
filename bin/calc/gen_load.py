#!/usr/bin/env python3

import sys
import os
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('loadfile', help='Target file containing loads.')
	return parser.parse_args()

def main():
	args = parse_args()
	lf = args.loadfile
	
	fin = open(lf, 'r')
	if not fin:
		sys.stderr.write('Fatal: cannot open load file: %s' % lf)
		return 2

	epoch = 0
	while True:
		line = fin.readline()
		if not line:	break
		line = line[:-1]

		items = line.strip().split()
		if items[0] == 'compute':
			epoch += 1
			sys.stdout.write('\n%d\t' % epoch)
			continue

		load = float(items[2])
		sys.stdout.write('%.2f\t' % load)

	sys.stdout.write('\n')

	fin.close()

if __name__ == '__main__':
	sys.exit(main())
