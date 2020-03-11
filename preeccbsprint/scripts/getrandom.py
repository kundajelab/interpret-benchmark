#!/usr/bin/python

#script written by Eva Prakash to randomly sample lines from a fasta file
#modified slightly for determinism and to read from gzipped files

import sys
import os
import random
import gzip

if len(sys.argv) < 4:
	print("Usage: {} filename number_of_sequences_to_randomly_extract random_seed".format(sys.argv[0]))
	exit(1)

filename = sys.argv[1]
number = int(sys.argv[2])
seed = int(sys.argv[3])
random.seed(seed)
numlines = int(os.popen("wc -l {} | cut -d ' ' -f 1".format(filename)).read())/2
linenums = random.sample(range(0, numlines), number)
linenums.sort()
if (".gz" in filename):
    fp = gzip.open(filename, "r")
else:
    fp = open(filename, "r")
array_position=0
current_line=0
skip_next = False
print_next = False
should_exit = False
for line in fp:
	if skip_next:
		if print_next:
			print(line.strip("\n"))
		skip_next = False
		if should_exit:
			fp.close()
			exit(0)
	else:
		if (linenums[array_position] == current_line):
			print(line.strip("\n"))
			array_position=array_position+1
			skip_next = True
			print_next = True
			if (array_position >= len(linenums)):
				should_exit = True
		else:
			skip_next = True
			print_next = False
		current_line = current_line+1
fp.close()
