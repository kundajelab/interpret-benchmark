#!/usr/bin/env bash

INP_FILE_PATHS="data_paths.txt"
ALL_NAIVE_PEAKS="all_naive_peaks.bed.gz"
MERGED_NAIVE_PEAKS="merged_naive_peaks.bed.gz"
ALL_BINS="all_bins.bed.gz"

[[ -e $ALL_NAIVE_PEAKS ]] && rm $ALL_NAIVE_PEAKS
[[ -e $MERGED_NAIVE_PEAKS ]] && rm $MERGED_NAIVE_PEAKS
[[ -e $ALL_BINS ]] && rm $ALL_BINS

#concatenate all the naive overlap peaks
if [ -e $ALL_NAIVE_PEAKS ]; then rm $ALL_NAIVE_PEAKS; fi
while IFS='' read -r line || [[ -n "$line" ]]; do
    task_name=$(echo $line | cut -d" " -f1)
    idr_path=$(echo $line | cut -d" " -f2)
    naive_path=$(echo $line | cut -d" " -f3)
    zcat $naive_path | gzip -c >> $ALL_NAIVE_PEAKS
done < $INP_FILE_PATHS


#run bedtools merge
zcat $ALL_NAIVE_PEAKS | sortBed | mergeBed | gzip -c > $MERGED_NAIVE_PEAKS

#create the bins
zcat $MERGED_NAIVE_PEAKS | perl -lane '$bins_start=50*int($F[1]/50); $bins_end=50*int($F[2]/50); for (my $i=$bins_start; $i <= $bins_end; $i+=50) {print($F[0]."\t".$i."\t".($i+200))}' | sortBed | uniq | gzip -c >> $ALL_BINS

echo "number of bins"
zcat $ALL_BINS | wc -l

#do a bedtools intersect with all the naive peaks and idr peaks
while IFS='' read -r line || [[ -n "$line" ]]; do
    task_name=$(echo $line | cut -d" " -f1)
    idr_path=$(echo $line | cut -d" " -f2)
    naive_path=$(echo $line | cut -d" " -f3)

    [[ -d $task_name ]] || mkdir $task_name
    echo $task_name
    intersectBed -e -f 0.5 -F 0.5 -a $ALL_BINS -b $idr_path -wa | gzip -c > $task_name/idr_optimal_overlaps.bed.gz
    echo "idr optimal regions"
    zcat $task_name/idr_optimal_overlaps.bed.gz | wc -l
    intersectBed -e -f 0.5 -F 0.5 -a $ALL_BINS -b $naive_path -wa | gzip -c > $task_name/naive_overlaps.bed.gz
    echo "naive regions"
    zcat $task_name/naive_overlaps.bed.gz | wc -l
done < $INP_FILE_PATHS
