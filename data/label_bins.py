#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import gzip

data_paths_file = "data_paths.txt"
all_bins_file = "all_bins.bed.gz"
file_name_within_folder = "naive_overlaps.bed.gz"
chromsizes_file = "hg19.chrom.sizes"


def label_bins(options):
    
    #read the data_paths folders
    folders = [x.rstrip().split(" ")[0] for x in open(data_paths_file)]

    folder_to_regions = {}
    for folder in folders:
        folder_to_regions[folder] = set([
            "_".join(x.rstrip().split("\t")[0:3])
            for x in
            gzip.open(folder+"/"+file_name_within_folder, 'rb')])

    #read in the chromosome sizes
    chrom_to_size = dict([x.rstrip().split("\t")
                          for x in open(chromsizes_file)])

    outfh = open(options.output_file, 'w') 
    for line in gzip.open(all_bins_file, 'rb'):
        chrom,start,end = line.rstrip().split("\t")[0:3]
        chrom_start_end = chrom+"_"+start+"_"+end
        start = int(start)
        end = int(end)
        expanded_start = start-options.flank_expansion
        expanded_end = end+options.flank_expansion
        if (expanded_start > 0 and expanded_end < chrom_to_size[chrom]):
            labels = [("1" if chrom_start_end
                           in folder_to_regions[folder] else "0")
                      for folder in folders] 
            outfh.write(chrom+"\t"+str(expanded_start)
                        +"\t"+str(expanded_end)+"\t"+("\t".join(labels))+"\n")
    
    outfh.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_file")
    parser.add_argument("--flank_expansion", default=400)
    options = parser.parse_args()
    label_bins(options)
