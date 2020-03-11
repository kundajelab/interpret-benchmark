#!/usr/bin/env bash

WINDOW_AROUND_SUMMIT_UNIVERSAL_PEAKS="merged_universal_neg_representative_peaks.bed.gz"
INP_FILE_PATHS="data_paths.txt"

if [ ! -e $WINDOW_AROUND_SUMMIT_UNIVERSAL_PEAKS ]; then 
    ./prep_representative_universal_negatives.sh
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
    zcat $naive_path | perl -lane 'print $F[0]."\t".(($F[1]+$F[9]))."\t".(($F[1]+$F[9]))."\t1"' | bedtools slop -g hg19.chrom.sizes -b 500 | perl -lane 'if ($F[2]-$F[1]==1000) {print $_}' | sortBed | gzip -c > $task_naive_window_around_summit 
    intersectBed -sorted -v -a $WINDOW_AROUND_SUMMIT_UNIVERSAL_PEAKS -b $task_naive_window_around_summit -wa | perl -lane 'print($F[0]."\t".$F[1]."\t".$F[2]."\t0")' | gzip -c > $task_negatives 
    
    task_labels=$task_name"/labels.gz"
    zcat $task_naive_window_around_summit | gzip -c > $task_labels
    zcat $task_negatives | gzip -c >> $task_labels

    zcat $task_negatives | egrep -v -w "chr1|chr2" | gzip -c > $task_name"/train_negatives.gz"
    zcat $task_naive_window_around_summit | egrep -v -w "chr1|chr2" | gzip -c > $task_name"/train_positives.gz"

    zcat $task_labels | egrep -w 'chr2' | gzip -c > $task_name"/valid_labels.gz"
    zcat $task_labels | egrep -w 'chr1' | gzip -c > $task_name"/test_labels.gz"
    zcat $task_name"/test_labels.gz" | perl -lane 'if ($F[3]==1) {print $_}' | gzip -c > $task_name"/positive_test_examples.gz"

done < $INP_FILE_PATHS

