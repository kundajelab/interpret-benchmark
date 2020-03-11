#!/usr/bin/env python
#Written by Eva Prakash

import sys
import re
from deeplift import dinuc_shuffle as dn

if len(sys.argv) < 2:
	print("Usage: {} filename".format(sys.argv[0]))
	exit(1)

filename = sys.argv[1]
fp = open(filename, "r")
expecting = "label"
label=''
for line in fp:
	if expecting == "label":
		match = re.match(">(.*)$", line)
		if match:
			label = match.group(1)
			expecting = "sequence"
		else:
			print("Expecting LABEL but found (!!): " + line)
			continue
	else:
		match = re.match("(\w+)$", line)
		if match:
			sequence = match.group(1)
			dinuc_sequence = dn.dinuc_shuffle(sequence)
			print(">dinuc_shuff_{}".format(label))
			print(dinuc_sequence)
		else:
			print("Expecting SEQUENCE but found (!!): " + line)
		expecting = "label"
fp.close()

