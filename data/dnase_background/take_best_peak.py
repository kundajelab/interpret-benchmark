#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import gzip

def take_best_peak(options):
    rank_col = options.col_to_rank_by 
    fh = gzip.open(options.infile,"rb") 
    best_seen_deets = None #(chrom, summit, peak_height)
    last_region_id = None
    for line in fh:
        if (hasattr(line, 'decode')):
            line = line.decode("utf-8")
        line_arr = line.rstrip().split("\t")
        region_id = "_".join(line_arr[0:3]) #regionid is chr_start_end
        current_peak_deets = line_arr[3:13]
        #summit = int(line_arr[4])+int(line_arr[12]) #summit = start + offset

        #The input lines are sorted such that overlapping regions have
        # the same region_id and come one after the other. If the next
        # region_id is not the same as the previous region_id, then
        # you have finished seeing a set of overlapping regions.
        #Write out the details for the highest peak seen in the set.
        if region_id != last_region_id:
            if (last_region_id is not None):
                print("\t".join(best_seen_deets))
            #reset best_seen_deets
            best_seen_deets = current_peak_deets
            last_region_id = region_id 
        #peak height is 7th col of narrowpeak file
        if (float(current_peak_deets[6]) > float(best_seen_deets[6])): 
            best_seen_deets = current_peak_deets
    #At the end of the file, make sure we remember to write out the
    # best peak for the last set
    print("\t".join(best_seen_deets))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--col_to_rank_by", default=9, help="Zero indexed") 
    parser.add_argument("--infile") 
    options = parser.parse_args()
    take_best_peak(options)
