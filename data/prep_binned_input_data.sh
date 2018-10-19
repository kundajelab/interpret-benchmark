#!/usr/bin/env bash

INP_FILE_PATHS="data_paths.txt"
ALL_NAIVE_PEAKS="all_naive_peaks.bed.gz"

#concatenate all the naive overlap peaks
if [ -e $ALL_NAIVE_PEAKS ]; then rm $ALL_NAIVE_PEAKS; fi
while IFS='' read -r line || [[ -n "$line" ]]; do
    task_name=$(echo $line | cut -d" " -f1)
    idr_path=$(echo $line | cut -d" " -f2)
    naive_path=$(echo $line | cut -d" " -f3)
    zcat $naive_path | gzip -c >> $ALL_NAIVE_PEAKS
done < $INP_FILE_PATHS

MERGED_NAIVE_PEAKS="merged_naive_peaks.bed.gz"

#run bedtools merge
zcat $ALL_NAIVE_PEAKS | sortBed | mergeBed | gzip -c > merged_naive_peaks.bed.gz
