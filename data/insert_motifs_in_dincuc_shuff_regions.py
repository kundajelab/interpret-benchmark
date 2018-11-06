#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import gzip
from Bio import SeqIO
from deeplift.dinuc_shuffle import dinuc_shuffle
from collections import namedtuple

import numpy as np
import random
random.seed(1234)
np.random.seed(1234)

MotifHit = namedtuple("MotifHit", ["region_id", "offset", "motif_seq",
                                   "motif_strand",
                                   "motif_score",
                                   "motif_sig",
                                   "motif_id", "motif_factor"])
rc_map = {'A': 'T', 'C': 'G', 'G': 'C', 'T':'A'}
def revcomp(seq):
    return "".join([rc_map[x] for x in seq[::-1]])

def parse_motif_line(motif_line):
    dat = motif_line.rstrip().split("\t")
    motif_strand = dat[7]
    return MotifHit(region_id=dat[0]+":"+dat[1]+"-"+dat[2],
                    offset=(int(dat[5])-1)-int(dat[1]),
                    motif_strand=motif_strand,
                    motif_id=dat[8],
                    motif_factor=dat[9],
                    motif_score=float(dat[10]),
                    motif_sig=float(dat[11]),
                    motif_seq=(dat[12].upper() if motif_strand=="+"
                               else revcomp(dat[12].upper())))

def insert_motifs_in_dincuc_shuff_regions(options):
    motif_hits_file = options.motif_hits_file 
    sequence_file = options.sequence_file
    sigthreshold = options.sigthreshold

    fasta_sequences = SeqIO.parse(gzip.open(sequence_file, 'rb'),'fasta')
    motif_fh = gzip.open(motif_hits_file)
    motif_hit = parse_motif_line(motif_fh.next())
    for fasta in fasta_sequences:
        region_id, orig_sequence = fasta.id, fasta.seq.tostring()
        region_chrom = region_id.split(":")[0]
        region_start,region_end = (region_id.split(":")[1]).split("-")
        orig_sequence = orig_sequence.upper()
        shuffled_seq_arr = [x for x in dinuc_shuffle(orig_sequence).lower()] 
        inserted_motifs = []
        while (motif_hit is not None and motif_hit.region_id==region_id):
            #insert motif into shuffled seq 
            if (motif_hit.offset >= 0 and
                (motif_hit.offset+len(motif_hit.motif_seq))
                 <= len(shuffled_seq_arr) and
                motif_hit.motif_sig < sigthreshold):
                orig_seq_snippet = orig_sequence[
                                        motif_hit.offset:
                                        (motif_hit.offset+
                                         len(motif_hit.motif_seq))]
                assert orig_seq_snippet==motif_hit.motif_seq, orig_seq_snippet+" vs "+motif_hit.motif_seq 
                shuffled_seq_arr[
                 motif_hit.offset:(motif_hit.offset+
                  len(motif_hit.motif_seq))] = motif_hit.motif_seq
                inserted_motifs.append(motif_hit)
            #read the next motif, if available
            try:
                motif_hit = parse_motif_line(motif_fh.next())
            except(StopIteration):
                motif_hit = None
        shuffled_seq = "".join(shuffled_seq_arr)
        print(region_chrom+"\t"+region_start+"\t"+region_end+"\t"
              +region_id+"\t"+shuffled_seq+"\t"+
              (";".join([str(x.offset)
                         +","+x.motif_id
                         +","+x.motif_factor
                         +","+str(x.motif_seq)
                         +","+str(x.motif_strand)
                         +","+str(x.motif_sig)
                         for x in inserted_motifs])))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--motif_hits_file", required=True)
    parser.add_argument("--sequence_file", required=True)
    parser.add_argument("--sigthreshold", type=float, required=True)
    options = parser.parse_args()
    insert_motifs_in_dincuc_shuff_regions(options)
