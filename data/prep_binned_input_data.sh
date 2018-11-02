#!/usr/bin/env bash

MERGED_UNIVERSAL_PEAKS="merged_universal_negatives.bed.gz"
INP_FILE_PATHS="data_paths.txt"
#ALL_NAIVE_PEAKS="all_naive_peaks.bed.gz"
#MERGED_NAIVE_PEAKS="merged_naive_peaks.bed.gz"
FILE_TO_BIN=$MERGED_UNIVERSAL_PEAKS
ALL_BINS="all_bins.bed.gz"
LABELS_OUT="all_labels.bed"

if [ ! -e $MERGED_UNIVERSAL_PEAKS ]; then 
    mergeBed -i /srv/scratch/annashch/deeplearning/gecco/encode_dnase/all_dnase_idr_peaks.sorted.bed | gzip -c > merged_universal_negatives.bed.gz
fi

#Create union of all naive peaks
#[[ -e $ALL_NAIVE_PEAKS ]] && rm $ALL_NAIVE_PEAKS
#[[ -e $MERGED_NAIVE_PEAKS ]] && rm $MERGED_NAIVE_PEAKS
#
##concatenate all the naive overlap peaks
#if [ -e $ALL_NAIVE_PEAKS ]; then rm $ALL_NAIVE_PEAKS; fi
#while IFS='' read -r line || [[ -n "$line" ]]; do
#    task_name=$(echo $line | cut -d" " -f1)
#    idr_path=$(echo $line | cut -d" " -f2)
#    naive_path=$(echo $line | cut -d" " -f3)
#    zcat $naive_path | gzip -c >> $ALL_NAIVE_PEAKS
#done < $INP_FILE_PATHS
#
##run bedtools merge
#zcat $ALL_NAIVE_PEAKS | sortBed | mergeBed | gzip -c > $MERGED_NAIVE_PEAKS

##create the bins
#[[ -e $ALL_BINS ]] && rm $ALL_BINS
#zcat $FILE_TO_BIN | perl -lane '$bins_start=50*int($F[1]/50); $bins_end=50*int($F[2]/50); for (my $i=$bins_start; $i <= $bins_end; $i+=50) {print($F[0]."\t".$i."\t".($i+200))}' | sortBed | uniq | gzip -c >> $ALL_BINS
#
#echo "number of bins"
#zcat $ALL_BINS | wc -l

#do a bedtools intersect with all the naive peaks and idr peaks
while IFS='' read -r line || [[ -n "$line" ]]; do
    task_name=$(echo $line | cut -d" " -f1)
    idr_path=$(echo $line | cut -d" " -f2)
    naive_path=$(echo $line | cut -d" " -f3)

    echo "Number of naive peaks for" $task_name
    zcat $naive_path | wc -l
    echo "Number of idr peaks for" $task_name
    zcat $idr_path | wc -l

    [[ -d $task_name ]] || mkdir $task_name
    echo $task_name
    intersectBed -e -f 0.5 -F 0.5 -a $ALL_BINS -b $idr_path -wa | gzip -c > $task_name/idr_optimal_overlaps.bed.gz
    echo "idr optimal regions"
    zcat $task_name/idr_optimal_overlaps.bed.gz | wc -l
    intersectBed -e -f 0.5 -F 0.5 -a $ALL_BINS -b $naive_path -wa | gzip -c > $task_name/naive_overlaps.bed.gz
    echo "naive regions"
    zcat $task_name/naive_overlaps.bed.gz | wc -l
done < $INP_FILE_PATHS

echo "preparing labels file"

./label_bins.py $LABELS_OUT
gzip $LABELS_OUT

zcat $LABELS_OUT".gz" | egrep -w 'chr1|chr8|chr21' | gzip -c > "test_"$LABELS_OUT".gz"
zcat $LABELS_OUT".gz" | egrep -w 'chr9' | gzip -c > "valid_"$LABELS_OUT".gz"
zcat $LABELS_OUT".gz" | egrep -w -v 'chr1|chr8|chr21|chr9' | gzip -c > "train_"$LABELS_OUT".gz"
zcat valid_all_labels.bed.gz | perl -lane 'if ($.%10 == 1) {print $_}' | gzip -c > small_valid_all_labels.bed.gz
