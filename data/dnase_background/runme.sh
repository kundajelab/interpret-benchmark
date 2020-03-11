#!/usr/bin/env bash

alldnase_background=/srv/scratch/annashch/deeplearning/gecco/encode_dnase/all_dnase_idr_peaks.sorted.bed

#mergeBed will create a single peak for each set of overlapping peaks
cat $alldnase_background | mergeBed | gzip -c > merged_alldnase_bg.bed.gz

#This bedtools intersect command will then record the 'merged' peak corresponding
# to each individual peak. 
bedtools intersect -sorted -a merged_alldnase_bg.bed.gz -b $alldnase_background -wa -wb | gzip -c > merged_alldnase_bg_intersected.bed.gz

#take_best_peak.py will take the peak with the highest peak height corresponding
# to each set of overlapping peaks that are merged by mergeBed. It will write
# out +/- flank around the summit of the peak, where flank is 500
# by default.
./take_best_peak.py | gzip -c > merged_alldnase_bg_representative_peaks.bed.gz

#remove temp files
rm merged_alldnase_bg.bed.gz
rm merged_alldnase_bg_intersected.bed.gz
