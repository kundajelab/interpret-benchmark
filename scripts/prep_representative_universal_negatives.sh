#!/usr/bin/env bash

universal_negatives=/srv/scratch/annashch/deeplearning/gecco/encode_dnase/all_dnase_idr_peaks.sorted.bed
merged_universal_neg="merged_universal_neg.bed.gz"

cat $universal_negatives | mergeBed | gzip -c > $merged_universal_neg

bedtools intersect -sorted -a $merged_universal_neg -b $universal_negatives -wa -wb | gzip -c > merged_universal_neg_intersected.bed.gz

./take_best_peak.py | gzip -c > merged_universal_neg_representative_peaks.bed.gz

