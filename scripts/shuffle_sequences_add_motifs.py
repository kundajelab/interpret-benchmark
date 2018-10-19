#!/usr/bin/env python
#Written by Eva Prakash

import sys
import re
from deeplift import dinuc_shuffle as dn
from collections import OrderedDict
import argparse

def load_sequences(seqfile):
	seqs = OrderedDict()
	fp = open(seqfile, "r")
	print("#Loading " + seqfile + " ...")
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
				seqs[label]=sequence
			else:
				print("Expecting SEQUENCE but found (!!): " + line)
			expecting = "label"
			label=''
	fp.close()
	print("#Loaded " + str(len(seqs.keys())) + " sequences from " + seqfile)
	return seqs

def load_motif_matches(motif_match_file):
	motif_matches = OrderedDict()
	fp = open(motif_match_file, "r")
	print("#Loading " + motif_match_file + " ...")
	numlines = 0
	for line in fp:
		match = re.match("((\w|\-)+)\s+((\w|\:|\-)+)\s+(\d+)\s+(\d+)\s+(\+|\-)\s+.+\s+(\w+)$", line)
		if match:
			numlines = numlines + 1
			motif = match.group(1)
			sequence = match.group(3)
			begin = int(match.group(5))
			end = int(match.group(6))
			strand = match.group(7)
			seqval = match.group(8)
			entry = dict()
			entry['motif'] = motif
			entry['sequence'] = sequence
			entry['begin'] = begin-1 # Homer motif match file is 1 indexed, convert to 0
			entry['end'] = end # Homer motif match file is 1 indexed AND inclusive, convert to 0 and exclusive
			entry['strand'] = strand
			entry['seqval'] = seqval
			if sequence not in motif_matches:
				motif_matches[sequence] = list()
			motif_matches[sequence].append(entry)
	fp.close()
	print("#Loaded " + str(numlines) + " motif matches in " + str(len(motif_matches.keys())) + " sequences")
	return motif_matches

def shuffle_seq_and_insert_motifs(seq, modlist, doprint=False):
	newseq = dn.dinuc_shuffle(seq)
	if doprint:
		print("Incoming sequence is " + seq)
	if modlist is not None:
		if doprint:
			print("Modlist " + str(modlist))
		for mod in modlist:
			begin = mod['begin']
			end = mod['end']
			newseq = newseq[0:begin] + seq[begin:end] + newseq[end:]
	if doprint:
		print("Outgoing sequence is " + newseq)
	return newseq

parser = argparse.ArgumentParser()
parser.add_argument("motifMatchFile", type=str,
                    help="File that contains motif matches and their positions")
parser.add_argument("sequenceFile", type=str,
		    help="File that contains FASTA sequences where motif matches were found")
args = parser.parse_args()

seqs = load_sequences(args.sequenceFile)
motif_matches = load_motif_matches(args.motifMatchFile)

for key in seqs:
	origseq = seqs[key]
	if key in motif_matches:
		modlist = motif_matches[key]
		newseq = shuffle_seq_and_insert_motifs(origseq, modlist)
	else:
		#print("!!! key missing: " + key)
		newseq = dn.dinuc_shuffle(origseq)
	print(">dinuc_shuffled_motifs_implanted_" + key)
	print(newseq)
