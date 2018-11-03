#!/usr/bin/env bash

WINDOW_AROUND_SUMMIT_UNIVERSAL_PEAKS="universal_negatives_window_around_summit.bed.gz"
INP_FILE_PATHS="data_paths.txt"

if [ ! -e $WINDOW_AROUND_SUMMIT_UNIVERSAL_PEAKS ]; then 
    cat /srv/scratch/annashch/deeplearning/gecco/encode_dnase/all_dnase_idr_peaks.sorted.bed | perl -lane 'print $F[0]."\t".(($F[1]+$F[9]))."\t".(($F[1]+$F[9]))' | bedtools slop -g hg19.chrom.sizes -b 500 | perl -lane 'if ($F[2]-$F[1]==1000) {print $_}' | gzip -c > $WINDOW_AROUND_SUMMIT_UNIVERSAL_PEAKS
fi

while IFS='' read -r line || [[ -n "$line" ]]; do
    task_name=$(echo $line | cut -d" " -f1)
    folder_path=$(echo $line | cut -d" " -f2)
    naive_path=`ls $folder_path"/macs2/overlap/"*.narrowPeak.gz`
    echo "naive overlap peaks path "$naive_path
    echo "Number of naive peaks for" $task_name
    zcat $naive_path | wc -l

    task_naive_window_around_summit=$task_name"/naive_window_around_summit.bed.gz"
    task_negatives=$task_name"/universal_negatives.bed.gz"

    [[ -d $task_name ]] || mkdir $task_name
    zcat $naive_path | perl -lane 'print $F[0]."\t".(($F[1]+$F[9]))."\t".(($F[1]+$F[9]))."\t1"' | bedtools slop -g hg19.chrom.sizes -b 500 | perl -lane 'if ($F[2]-$F[1]==1000) {print $_}' | gzip -c > $task_naive_window_around_summit 
    intersectBed -v -a $WINDOW_AROUND_SUMMIT_UNIVERSAL_PEAKS -b $task_naive_window_around_summit -wa | perl -lane 'print($F[0]."\t".$F[1]."\t".$F[2]."\t0")' | gzip -c > $task_negatives 
    
    task_labels=$task_name"/labels.gz"
    zcat $task_naive_window_around_summit | gzip -c > $task_labels
    zcat $task_negatives | gzip -c >> $task_labels

    zcat $task_labels | egrep -w 'chr8|chrX' | gzip -c > $task_name"/valid_labels.gz"
    zcat $task_labels | egrep -w 'chrY' | gzip -c > $task_name"/test_labels.gz"
    zcat $task_name"/valid_labels.gz" | perl -lane 'if ($.%30==0) {print $_}' | gzip -c > $task_name"/small_valid_labels.gz"
    zcat $task_name"/valid_labels.gz" | perl -lane 'if ($.%30!=0 && $F[3]==1) {print $_}' | gzip -c > $task_name"/positives_not_in_small_valid_labels.gz"

done < $INP_FILE_PATHS

