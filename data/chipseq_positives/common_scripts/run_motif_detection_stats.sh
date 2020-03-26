#!/usr/bin/env bash

mkdir motif_detection_stats

model_ids_to_use_file="model_ids_to_use.txt"
input_seqs_file="sequences/test_sim_positives.txt.gz"

while IFS= read -r modelid
do
    echo "on id "$modelid
    compute_motif_detection_stats --sequences_and_motifs $input_seqs_file --interpretation_h5 interpretation/interpretation_$modelid.h5 --outfile motif_detection_stats/$modelid.json
done < $model_ids_to_use_file
