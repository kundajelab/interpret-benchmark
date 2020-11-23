#!/usr/bin/env python

import gzip
import numpy as np
import argparse

def load_sequences(seqfile):
    labels = []
    seqs = []
    fp = gzip.open(seqfile, "rb")
    print("#Loading " + seqfile + " ...")
    for line in fp:
        line=line.decode('utf8').split()
        labels.append(line[0])
        seqs.append(line[1])
    fp.close()
    print("#Loaded " + str(len(seqs)) + " sequences from " + seqfile)
    return labels, seqs

parser = argparse.ArgumentParser()
parser.add_argument("seqfile", type=str, help="File that contains FASTA sequences")
parser.add_argument("outfile", type=str, help="Output file")
args = parser.parse_args()
labels, seqs = load_sequences(args.seqfile)
fp = open(args.outfile, 'w+')
for i in range(len(seqs)):
    fp.write(">" + labels[i] + "\n" + seqs[i] + "\n")
fp.close()
