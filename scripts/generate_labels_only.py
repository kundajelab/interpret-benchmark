#!/usr/bin/python
#Written by Eva Prakash

import sys
import re

if len(sys.argv) < 2:
	print("Usage: {} filename".format(sys.argv[0]))
	exit(1)

filename = sys.argv[1]
fp = open(filename, "r")
for line in fp:
	match = re.match(">((dinuc_shuff_|dinuc_shuffled_).+)$", line)
	if match:
		value = 0
		chrom = match.group(1)
		if match.group(2) == 'dinuc_shuff_':
			value = 0
		else:
			value = 1
		print(chrom)
	else:
		continue
fp.close()

