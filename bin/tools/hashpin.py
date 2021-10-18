#!/usr/bin/env python3

import sys
import os
import argparse
import hashlib

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('direc', help='target dir')
	parser.add_argument('mdsamount', type=int, help='number of mds servers')
	parser.add_argument('depth', type=int, help='target depth')
	parser.add_argument('-u', '--unpin', action="store_true",  help='Unpin directory')
	return parser.parse_args()

def hash(fullpath, mdsamount):
	return int(hashlib.sha1(fullpath.encode('utf-8')).hexdigest(), 16) % mdsamount

def pin(direc, target_mds = -1):
	if not direc:	return
	os.system('setfattr -n ceph.dir.pin -v %d %s' % (target_mds, direc))

def hash_pin(root_direc, mdsamount, depth = 0, unpin=False):
	if os.path.isfile(root_direc): return
	sys.stdout.write('\r%d %s' % (depth, root_direc) + ' ' * 20)
	if depth == 0:
		pin(root_direc, unpin and -1 or hash(root_direc, mdsamount))
		return

	assert(os.path.isdir(root_direc))
	files = os.listdir(root_direc)
	for f in files:
		fullpath = os.path.join(root_direc, f)
		#print(fullpath)
		hash_pin(fullpath, mdsamount, depth - 1, unpin)

def main():
	# Parse args
	args = parse_args()

	hash_pin(args.direc, args.mdsamount, args.depth, args.unpin)
	print()
	return 0

if __name__ == '__main__':
	sys.exit(main())
