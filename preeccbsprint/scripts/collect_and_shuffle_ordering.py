#!/usr/bin/env python
#Written by Eva Prakash

import sys
import re
from collections import OrderedDict
import argparse
import random


def load_sequences(seqfile, num=-1):
	seqs = OrderedDict()
	fp = open(seqfile, "r")
	print("#Loading " + seqfile + " ...")
	expecting = "label"
	label=''
	numSeen = 0
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
				seqs[label]=sequence
				numSeen = numSeen+1
			else:
				print("Expecting SEQUENCE but found (!!): " + line)
			expecting = "label"
			label=''
		if num != -1 and numSeen >= num:
			break
	fp.close()
	print("#Loaded " + str(len(seqs.keys())) + " sequences from " + seqfile)
	return seqs

parser = argparse.ArgumentParser()
parser.add_argument("positiveSequenceFile", type=str,
                    help="File that contains positive (for training set)  FASTA sequences")
parser.add_argument("positiveNumber", type=int,
                    help="Number of positive sequences to take (-1 for all)")
parser.add_argument("negativeSequenceFile", type=str,
                    help="File that contains negative (for training set)  FASTA sequences")
parser.add_argument("negativeNumber", type=int,
                    help="Number of negative sequences to take (-1 for all)")

args = parser.parse_args()
seqs = load_sequences(args.positiveSequenceFile, args.positiveNumber)
seqs.update(load_sequences(args.negativeSequenceFile, args.negativeNumber))

total = len(seqs)
print("Got a total of " + str(total) + " sequences")

seqsAsList = seqs.items()
order = random.sample(range(total), total)

for i in order:
	item = seqsAsList[i]
	print(">" + item[0])
	print(item[1])
