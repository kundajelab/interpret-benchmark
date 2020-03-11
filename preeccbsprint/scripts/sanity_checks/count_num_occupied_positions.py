#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import sys
import os
from collections import defaultdict
import numpy as np

def count_num_occupied_positions(options):
    matches_file = options.matches_file
    seqlen = options.seqlen

    seq_id_to_occupied_positions = defaultdict(lambda: np.zeros(seqlen)) 
    matches_fh = open(matches_file)
    for line in matches_fh:
        _, seq_id, match_start, match_end, _, _, _ = line.rstrip().split("\t")
        match_start, match_end = int(match_start), int(match_end)
        seq_id_to_occupied_positions[seq_id][match_start:match_end] = 1.0 
    
    all_seq_arrs = np.array(list(seq_id_to_occupied_positions.values()))
    total_taken_positions = np.sum(all_seq_arrs)
    total_positions = np.sum([len(x) for x in all_seq_arrs])
    taken_fracs = [np.sum(x)/len(x) for x in all_seq_arrs]
    print("Total taken positions:",total_taken_positions)
    print("Total positions:",total_positions)
    print("Total taken frac:",total_taken_positions/total_positions)
    print("Median taken frac:",np.median(taken_fracs))
    print("Max taken frac:",np.max(taken_fracs))
    print("Min taken frac:",np.min(taken_fracs))
    print("90th percentile taken frac:",np.percentile(taken_fracs, 90))
    print("10th percentile taken frac:",np.percentile(taken_fracs, 10))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--matches_file", required=True) 
    parser.add_argument("--seqlen", required=True, type=int) 
    options = parser.parse_args()
    count_num_occupied_positions(options)
