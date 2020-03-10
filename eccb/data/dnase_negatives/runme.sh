#!/usr/bin/env bash

universal_negatives=/srv/scratch/annashch/deeplearning/gecco/encode_dnase/all_dnase_idr_peaks.sorted.bed

#mergeBed will create a single peak for each set of overlapping peaks
cat $universal_negatives | mergeBed | gzip -c > merged_universal_neg.bed.gz

#This bedtools intersect command will then record the 'merged' peak corresponding
# to each individual peak. 
bedtools intersect -sorted -a merged_universal_neg.bed.gz -b $universal_negatives -wa -wb | gzip -c > merged_universal_neg_intersected.bed.gz

#take_best_peak.py will take the peak with the highest peak height corresponding
# to each set of overlapping peaks that are merged by mergeBed. It will write
# out +/- flank around the summit of the peak, where flank is 500
# by default.
./take_best_peak.py | gzip -c > merged_universal_neg_representative_peaks.bed.gz

#remove temp files
rm merged_universal_neg.bed.gz
rm merged_universal_neg_intersected.bed.gz
