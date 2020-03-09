#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import gzip

infile = "merged_universal_neg_intersected.bed.gz"
chroms_file = "hg19.chrom.sizes"
chrom_to_size = dict([(x.rstrip().split("\t")[0],
                       int(x.rstrip().split("\t")[1]))
                       for x in open(chroms_file)])

def take_best_peak(options):
    rank_col = options.col_to_rank_by 
    fh = gzip.open(infile,"rb") 
    best_seen_deets = None #(chrom, summit, peak_height)
    last_region_id = None
    for line in fh:
        if (hasattr(line, 'decode')):
            line = line.decode("utf-8")
        line_arr = line.rstrip().split("\t")
        chrom = line_arr[0]
        region_id = "_".join(line_arr[0:3]) #regionid is chr_start_end
        peak_height = float(line_arr[9])
        summit = int(line_arr[4])+int(line_arr[12]) #summit = start + offset
        #The input lines are sorted such that overlapping regions have
        # the same region_id and come one after the other. If the next
        # region_id is not the same as the previous region_id, then
        # you have finished seeing a set of overlapping regions.
        #Write out the details for the highest peak seen in the set.
        if region_id != last_region_id:
            if (best_seen_deets is not None):
                #The region that is written out is +/- options.flank around
                # the summit. We want to avoid writing out regions that go
                # over the ends of the chromosome.
                if ((best_seen_deets[1] > options.flank) and
                    (best_seen_deets[1] <
                     (chrom_to_size[best_seen_deets[0]]-options.flank))):
                    print(best_seen_deets[0]+"\t"
                          +str(best_seen_deets[1]-options.flank)+"\t"
                          +str(best_seen_deets[1]+options.flank)+"\t"
                          +str(best_seen_deets[2]))
            best_seen_deets = [chrom,summit,peak_height] 
            last_region_id = region_id 
        if (peak_height > best_seen_deets[2]):
            best_seen_deets = [chrom,summit,peak_height]
    #Write out the details for the best peak for the last set of
    # overlapping region
    if ((best_seen_deets[1] > options.flank) and
        (best_seen_deets[1] <
         (chrom_to_size[best_seen_deets[0]]-options.flank))):
        print(best_seen_deets[0]+"\t"
              +str(best_seen_deets[1]-options.flank)+"\t"
              +str(best_seen_deets[1]+options.flank)+"\t"
              +str(best_seen_deets[2]))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--col_to_rank_by", default=9, help="Zero indexed") 
    parser.add_argument("--flank", default=500) 
    options = parser.parse_args()
    take_best_peak(options)
