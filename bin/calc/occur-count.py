#!/usr/bin/env python3

import sys
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', help='input file')
	return parser.parse_args().infile

def main():
	collector = {}
	fin_path = parse_args()
	with open(fin_path, 'r') as fin:
		while True:
			line = fin.readline()
			if not line:	break
			line = line.strip()
			try:
				collector[line] += 1
			except KeyError:
				collector[line] = 1

	for key, value in collector.items():
		print('%s\t%d' % (key, value))

if __name__ == '__main__':
	sys.exit(main())
