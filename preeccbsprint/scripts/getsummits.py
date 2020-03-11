#!/usr/bin/env python
#Written by Eva Prakash

import sys
import re

if len(sys.argv) < 2:
	print("Usage: {} filename".format(sys.argv[0]))
	exit(1)

filename = sys.argv[1]
fp = open(filename, "r")
for line in fp:
	match = re.match("(\w+)\s+(\d+)\s+(\d+)\s+.*\s+(\d+)$", line)
	if match:
		chrom = match.group(1)
		chromstart = int(match.group(2))
		chromend = int(match.group(3))
		offset = int(match.group(4))
		summitstart = chromstart + offset - 500
		summitend = chromstart + offset + 500
		print("{0}\t{1}\t{2}".format(chrom, summitstart, summitend))
	else:
		print("Rejecting line: " + line)
fp.close()

